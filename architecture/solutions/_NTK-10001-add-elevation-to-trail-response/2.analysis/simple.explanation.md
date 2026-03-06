# NTK-10001 - Simple Explanation

## What is the Problem

The NovaTrek trail API returns information about each trail such as distance and estimated hiking duration, but it does not include elevation data. Rangers and trip planners need to know how much elevation a trail gains and loses to properly assess difficulty and recommend appropriate gear to guests.

## What Changes

Two new data fields will be added to the trail API response:

- **Elevation Gain (meters)** - How much total uphill climbing the trail involves
- **Elevation Loss (meters)** - How much total downhill descent the trail involves

This data already exists in the database. The change simply exposes it through the API so applications can display it.

## Who is Impacted

- **Ranger staff** - Will see elevation data in the NovaTrek Guide App, eliminating the need to cross-reference separate spreadsheets
- **Trip planners** - Can factor elevation into difficulty assessments and gear recommendations
- **Guest-facing app** - Can display elevation information on the trail browser so guests know what to expect before booking

## Risk Level

**Low** - This is an additive change that adds new optional fields to an existing response. No existing fields are modified or removed. No database changes are required.
