# NTK-10001 - User Stories

## US1 - Trip Planner Views Elevation Data

**As a** trip planner,
**I want to** see elevation gain and loss for each trail in the system,
**so that I can** recommend appropriate difficulty levels and gear for guests booking adventure packages.

### Acceptance Criteria

- The trail API response includes elevation gain in meters
- The trail API response includes elevation loss in meters
- Elevation values are shown as null when data is not yet available for a trail
- Elevation data is available on both the single trail and trail list endpoints

## US2 - Guest Views Elevation in Trail Browser

**As a** guest browsing trails in the NovaTrek app,
**I want to** see elevation gain and loss information for a trail,
**so that I can** prepare physically and bring appropriate gear for the adventure.

### Acceptance Criteria

- Elevation data is available through the trail API for the guest-facing app to display
- Trails without elevation data do not show misleading default values (null is acceptable)
- The data is consistent with what rangers and trip planners see in internal tools
