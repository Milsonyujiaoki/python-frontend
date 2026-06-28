"""File handling utilities for Streamlit application."""

import streamlit as st
import pandas as pd
import io
from typing import Optional, Dict, Any, List


def upload_file(
    label: str = "Upload file",
    file_types: Optional[List[str]] = None,
    max_size_mb: int = 200,
    key: Optional[str] = None,
) -> Optional[Any]:
    """
    File upload helper with configuration.

    Args:
        label: Label for the uploader
        file_types: List of allowed extensions (e.g., ['csv', 'xlsx'])
        max_size_mb: Maximum file size in megabytes
        key: Streamlit key for the uploader

    Returns:
        Uploaded file object or None
    """
    if file_types is None:
        file_types = ["csv"]

    uploaded_file = st.file_uploader(
        label,
        type=file_types,
        help=f"Maximum file size: {max_size_mb}MB",
        key=key,
    )

    return uploaded_file


def load_csv_data(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Load CSV data from uploaded file.

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        DataFrame or None if loading fails
    """
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return None


def load_excel_data(
    uploaded_file, sheet_name: Optional[str] = None
) -> Optional[pd.DataFrame]:
    """
    Load Excel data from uploaded file.

    Args:
        uploaded_file: Streamlit uploaded file object
        sheet_name: Specific sheet name or None for first sheet

    Returns:
        DataFrame or None if loading fails
    """
    try:
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        return df
    except Exception as e:
        st.error(f"Error loading Excel: {str(e)}")
        return None


def download_csv_button(
    data: List[Dict[str, Any]],
    label: str = "📥 Download CSV",
    filename: str = "data.csv",
    use_container_width: bool = True,
) -> None:
    """
    Render a download button for CSV data.

    Args:
        data: List of dictionaries to convert to CSV
        label: Button label
        filename: Download filename
        use_container_width: Button width setting
    """
    if not data:
        st.warning("No data available for download")
        return

    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=use_container_width,
    )


def download_excel_button(
    data: List[Dict[str, Any]],
    label: str = "📥 Download Excel",
    filename: str = "data.xlsx",
    use_container_width: bool = True,
) -> None:
    """
    Render a download button for Excel data.

    Args:
        data: List of dictionaries to convert to Excel
        label: Button label
        filename: Download filename
        use_container_width: Button width setting
    """
    if not data:
        st.warning("No data available for download")
        return

    df = pd.DataFrame(data)

    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")

    output.seek(0)

    st.download_button(
        label=label,
        data=output.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=use_container_width,
    )


def import_data_modal(
    key: str = "import_data",
    supported_types: Optional[List[str]] = None,
    on_import: Optional[callable] = None,
) -> None:
    """
    Render a modal-like section for data import.

    Args:
        key: Session state key
        supported_types: List of supported file types
        on_import: Callback function when data is imported
    """
    if supported_types is None:
        supported_types = ["csv", "xlsx"]

    if st.session_state.get(f"show_{key}", False):
        st.markdown("---")
        st.subheader("📥 Import Data")

        uploaded_file = upload_file(
            label="Select file to import",
            file_types=supported_types,
            key=f"{key}_uploader",
        )

        if uploaded_file:
            st.info(f"Selected: {uploaded_file.name}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Process Import", use_container_width=True):
                    if "csv" in uploaded_file.name.lower():
                        df = load_csv_data(uploaded_file)
                    elif any(
                        ext in uploaded_file.name.lower()
                        for ext in ["xlsx", "xls"]
                    ):
                        df = load_excel_data(uploaded_file)
                    else:
                        st.error("Unsupported file format")
                        df = None

                    if df is not None:
                        st.success(f"Loaded {len(df)} rows")
                        if on_import:
                            on_import(df)
                        st.session_state[f"show_{key}"] = False
                        st.rerun()

            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state[f"show_{key}"] = False
                    st.rerun()


def export_data_with_options(
    data: List[Dict[str, Any]], title: str = "Export Data"
) -> None:
    """
    Render export options for data.

    Args:
        data: Data to export
        title: Section title
    """
    with st.expander(f"📥 {title}", expanded=False):
        st.markdown("**Select export format:**")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("CSV", use_container_width=True):
                download_csv_button(data, filename="export.csv")

        with col2:
            if st.button("Excel", use_container_width=True):
                download_excel_button(data, filename="export.xlsx")

        with col3:
            if st.button("JSON", use_container_width=True):
                import json
                json_data = json.dumps(data, indent=2)
                st.download_button(
                    label="JSON",
                    data=json_data,
                    file_name="export.json",
                    mime="application/json",
                    use_container_width=True,
                )