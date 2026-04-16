# MiniTV Requirements

## REQ-001: HomeAssistant-Triggered Display Yellow Flash Alert

**Status:** In Progress

**Description:**
Implement a yellow flash alert function that:
- Listens for trigger events from HomeAssistant (binary_sensor, event, or API call)
- Flashes the display yellow (set color to yellow in the display lambda)
- Displays custom text provided by the trigger (e.g., "Door Opened", "Motion Detected")
- Maintains the flash and text display for 5 seconds (no timeout during flash)
- Returns to normal display state (clock) after 5 seconds

**Implementation Details:**
- Use HomeAssistant service calls or `api:` component to trigger from HA integration
- Store alert state (active status, text, timestamp) in global variables
- Modify display lambda to check alert state and render alert when active
- Example use case: binary_sensor (door open) triggers `"Door is opened"` alert on display

**Traceability:**
- Implementation: [MiniTV.yaml](../MiniTV.yaml) - global variables, API endpoint, display lambda
