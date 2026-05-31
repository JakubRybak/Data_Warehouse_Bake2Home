# Google Maps Integration & Search Grid Specifications

## Problem Assumptions
* The **Google Places API (New)** has a **Nearby Search** endpoint that filters by place types, accepts center coordinates and a search radius, and scans the circular area.
* Result limit per query: **20 places** (max).
* Assumption: All active customers are located within designated operational delivery zones (`Locations`).

## Goal
* Identify all direct (bakeries) and indirect (supermarkets) competitors within all operational delivery zones plus a defined safety **buffer** (3000m).

## Proposed Algorithm Flow
1. **Retrieve Locations**: Load active delivery zones from the operational database (filtering out empty or inactive regions).
2. **Merge Boundaries**: Merge adjacent or overlapping delivery zone polygons to create disjoint operational "islands".
3. **Apply Spatial Buffer**: Expand these islands by applying a safety buffer (3000m) to capture competitors in the surrounding delivery boundary.
4. **Resolve Overlaps**: Re-merge any islands that overlap after the buffering process to form the final set of disjoint geometries to cover.
5. **Hexagonal Grid Coverage**: Cover each final geometry with optimal search circles (using a standard 700m radius) using the **A4_Standard** algorithm.
6. **Query API**: For each generated circle center, make a call to the Google Places API.
7. **Business Filtering**: Deduplicate results, filter out generic convenience stores (e.g., Żabka, Carrefour Express), and classify competitors into `DIRECT` (bakeries) and `INDIRECT` (supermarkets) categories before saving.

---

## A4_Standard Algorithm

**Core Mechanics:**
1. **Hexagonal Grid Layout**: Arranges search circles in a honeycomb pattern. This is mathematically proven to be the most efficient way to cover a continuous 2D surface, minimizing circle overlap and completely eliminating gaps.
2. **Spatial Alignment Optimization**: Rather than applying a fixed grid statically, the algorithm dynamically evaluates dozens of grid alignments by performing:
   * **Rotation**: Rotating the search grid at different angles from 0° to 60° (using 7 rotation steps).
   * **Translation**: Shifting the grid along X and Y axes using small offsets (a 4x4 translation matrix).
3. **Optimal Selection**: The algorithm calculates the circle count for every translation and rotation combination, selecting the exact configuration that yields the **absolute minimum number of search circles** while guaranteeing 100% spatial coverage of the buffered polygon.
