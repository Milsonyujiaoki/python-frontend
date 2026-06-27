# Reflex Framework Best Practices

This document outlines best practices and patterns for developing with the Reflex framework in the context of the Barbershop SaaS application.

## Project Structure

The Reflex frontend follows a specific structure to maintain clarity and scalability:

```
frontend/reflex/
├── .web/                 # Vite/React build configuration and dependencies
├── components/           # Reusable UI components (forms, modals, tables, etc.)
├── pages/                # Page components (organized by feature)
├── states/               # Reflex state management (ReflexAuthState, etc.)
├── styles/               # Global styles and CSS utilities
└── tests/                # Unit and E2E tests
```

## State Management

### Reflex State Principles
- All application state should be managed through Reflex State classes
- State variables should be kept minimal and focused on UI concerns
- Use computed vars for derived state to avoid unnecessary recomputations
- Event handlers should return EventSpec (typically empty array `[]` for no navigation)

### Authentication State
The `ReflexAuthState` manages:
- Authentication tokens and user data
- Form state for login, registration, and password reset
- Loading and error states for async operations
- Helper methods for token management and user retrieval

## Component Development

### Reusable Components
- Place shared components in `/components` directory
- Components should be reusable and configurable via props
- Use Reflex's built-in components (rx.box, rx.vstack, rx.hstack) for layout
- Style components using Tailwind utility classes via the `class_name` prop

### Form Components
- Use the provided form components (`form_input`, `form_textarea`, etc.) for consistency
- All form components should handle required states and validation visually
- Event handlers for form inputs should update state via setter methods

### State Updates
- Update state through setter methods (e.g., `set_login_email(value)`)
- Avoid direct state mutation outside of event handlers
- Use `yield` for async operations to update loading states

## Styling and Theming

### Tailwind CSS
- The project uses Tailwind CSS for utility-first styling
- Customize the theme in `tailwind.config.js` if needed
- Use responsive prefixes (sm:, md:, lg:, xl:) for responsive design
- Apply dark mode variants where appropriate (`dark:`)

### Component Styling
- Prefer utility classes over custom CSS when possible
- For complex styling, create CSS modules in `/styles`
- Use the `style` prop for dynamic inline styles
- Leverage Reflex's color scheme support for light/dark modes

## Performance Optimization

### Bundle Optimization
- Use dynamic imports for code splitting where appropriate
- Lazy-load non-critical components and routes
- Optimize images and assets (use next-gen formats, proper sizing)
- Leverage browser caching for static assets

### State Updates
- Minimize state updates in rapid succession (e.g., during form input)
- Use debouncing for expensive operations triggered by user input
- Avoid large objects in state that cause deep equality checks

## Testing Strategy

### Unit Tests
- Test components in isolation using Python's unittest framework
- Mock event handlers and API interactions
- Verify component rendering with various props
- Test state transitions and event handler logic

### End-to-End Tests
- Use Playwright for critical user flows (login, navigation, form submissions)
- Test across multiple browsers (Chromium, Firefox, WebKit)
- Include responsive testing for mobile and desktop views
- Mock API responses where necessary to isolate frontend testing

## Development Workflow

### Local Development
- Start the development server with `reflex run` or `npm run dev` in `.web`
- Utilize hot module replacement for fast UI iteration
- Check linting and formatting with `ruff` and `black` (via pre-commit hooks)

### Production Build
- Build for production with `reflex export` or `npm run export`
- The optimized build is placed in the `/dist` directory
- Analyze bundle output to identify optimization opportunities
- Deploy the static assets to a CDN or web server

## Common Patterns

### Data Fetching
- Perform data fetching in event handlers or special methods
- Use loading states to provide feedback during async operations
- Handle errors gracefully with user-friendly messages

### Navigation
- Use `rx.redirect()` for programmatic navigation
- Leverage Reflex's automatic URL synchronization for state changes
- Protect routes requiring authentication in page components

### Error Handling
- Display user-friendly error messages using toast notifications
- Log errors to console for development visibility
- Provide retry mechanisms for recoverable errors

## Deployment Considerations

### Environment Variables
- Use `env.json` for runtime configuration
- Never store secrets in the frontend codebase
- Configure CORS properly on the backend for production domains

### Asset Optimization
- Enable compression (gzip/brotli) on the web server
- Set appropriate cache headers for static assets
- Use service workers for offline capabilities if needed

## Troubleshooting

### Common Issues
- **Hydration mismatches**: Ensure server-rendered and client-rendered content match
- **State not updating**: Verify event handlers return proper EventSpec
- **Styling issues**: Check Tailwind class names and responsive prefixes
- **Bundle size**: Analyze with `rollup-plugin-visualizer` or similar tools

### Debugging Tools
- Use browser devtools for inspecting React component tree
- Check Reflex console logs for state changes and events
- Utilize the Reflex debug panel if available in development