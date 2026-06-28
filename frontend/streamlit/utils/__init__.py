"""Utils package for Streamlit frontend."""

from .session_state import (
    initialize_session_state,
    set_authenticated,
    set_user,
    logout,
    set_customers,
    get_customers,
    set_barbers,
    get_barbers,
    set_services,
    get_services,
)

from .file_handler import (
    upload_file,
    load_csv_data,
    load_excel_data,
    download_csv_button,
    download_excel_button,
    import_data_modal,
    export_data_with_options,
)

from .cache import (
    cached_api_call,
    hash_data,
    get_cache_stats,
    clear_data_cache,
    clear_resource_cache,
    cached_computation,
    process_large_dataset,
    filter_and_sort_data,
    compute_metrics,
    generate_chart_data,
)

__all__ = [
    "initialize_session_state",
    "set_authenticated",
    "set_user",
    "logout",
    "set_customers",
    "get_customers",
    "set_barbers",
    "get_barbers",
    "set_services",
    "get_services",
    "upload_file",
    "load_csv_data",
    "load_excel_data",
    "download_csv_button",
    "download_excel_button",
    "import_data_modal",
    "export_data_with_options",
    "cached_api_call",
    "hash_data",
    "get_cache_stats",
    "clear_data_cache",
    "clear_resource_cache",
    "cached_computation",
    "process_large_dataset",
    "filter_and_sort_data",
    "compute_metrics",
    "generate_chart_data",
]