# NTK-10002: Simple Explanation

## The Problem

When a guest arrives at a NovaTrek check-in location, the system needs to know what kind of check-in experience to show them. Right now, it only looks at the broad activity type -- "hiking," "climbing," "kayaking," and so on. But that is like an airport sending every passenger through the same security line whether they are flying domestic economy or international first class with six checked bags. The needs are completely different.

A guest doing a simple day hike on a well-marked trail just needs to confirm their reservation and go. A guest doing a multi-day backcountry camping expedition needs to pick up specialized gear, meet their guide, coordinate transport to the trailhead, and complete a medical clearance form. Today, both of these guests see a check-in flow that tries to split the difference, and the result satisfies neither.

## The Solution

We are introducing a more granular classification system. Instead of 10 broad activity types, we will have 25 specific adventure categories. Each category maps to one of 3 check-in patterns:

- **Pattern 1 (Basic)**: A quick confirmation screen. In and out in 30 seconds. For simple activities like day hikes, bouldering, or birding safaris.
- **Pattern 2 (Gear Required)**: Confirmation plus a gear pickup step and safety briefing. About 3-5 minutes. For activities that involve specialized equipment, like kayaking or sport climbing.
- **Pattern 3 (Full Service)**: The complete check-in experience with gear pickup, guide meetup, transport details, and medical clearance. About 8-12 minutes. For complex, high-risk, or multi-day adventures.

Think of it like a hotel check-in: a returning loyalty member with a standard room gets express check-in, a first-time guest gets the normal process, and a guest in the presidential suite gets a personal concierge escort to their room. Same hotel, different experience based on what they need.

There are also two special rules based on how the trip was booked. Guests who booked through a partner organization always get the simple check-in, because the partner handles the rest. Walk-in guests always get the full check-in, because they have not done any pre-trip preparation.

## Why This Matters

The right check-in experience means day hikers are not frustrated by unnecessary steps, while backcountry adventurers get the thorough onboarding their safety depends on. It is about matching the process to the need.
