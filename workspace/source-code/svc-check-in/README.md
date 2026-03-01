# svc-check-in

Check-in processing service for NovaTrek Adventures. Handles guest check-ins across kiosk, staff, mobile, and partner tablet channels.

## Adventure Category Classification

The service classifies adventure categories into UI patterns that determine the check-in flow presented to guests:

| UI Pattern | Label | Description |
|------------|-------|-------------|
| PATTERN_1 | Standard | Simple check-in, no special requirements |
| PATTERN_2 | Safety Briefing | Requires a safety briefing before the activity |
| PATTERN_3 | Full Equipment | Requires full equipment check-out and training |

### Category Mappings

- **PATTERN_1**: Guided Nature Walk, Scenic Overlook, Bird Watching, Campfire Storytelling, Stargazing, Fishing Basic, Photography Tour, Wildflower Hike
- **PATTERN_2**: Mountain Hiking, Rock Climbing Intro, Mountain Biking, Horseback Trail, Cave Exploring, Zip Line, Cross Country Ski, Snowshoeing
- **PATTERN_3**: Whitewater Kayaking, Advanced Rock Climbing, Rappelling, Ice Climbing, Backcountry Ski, Paragliding, Canyoneering, Scuba Intro, Multi-Day Expedition

### Booking Source Overrides

Booking source takes precedence over category classification:

- **PARTNER_API** -> always PATTERN_1 (partner systems handle their own briefings)
- **WALK_IN** -> always PATTERN_3 (walk-ins receive the full safety and equipment flow)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/check-ins | Process a new check-in |
| GET | /api/v1/check-ins/{id} | Get a check-in record by ID |
| POST | /api/v1/check-ins/lookup-reservation | Lookup by confirmationCode + lastName |
| GET | /api/v1/check-ins/today?locationId= | Today's check-ins for a location |

## Configuration

Runs on port **8083**. Requires PostgreSQL and connectivity to `svc-reservations`.
