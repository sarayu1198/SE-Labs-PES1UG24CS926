# Use-Case Flow Specification

## Use Case: Lost-and-Found Matching

### Primary Actor
Finder / Owner

### Preconditions
1. A user has registered a lost item or a found item.
2. The item report contains the required category, color, description, and location information.
3. The system has active lost and found item reports available for comparison.

### Postconditions
1. The system identifies potential matches between lost and found items.
2. A match probability is calculated for compatible items.
3. The potential owner is notified when a sufficiently strong match is found.

### Main Success Scenario
1. The user submits a new lost-item or found-item report.
2. The system records the item details.
3. The system extracts relevant item tags such as category and color.
4. The system searches active reports for potentially matching items.
5. The system compares the category and color tags of the items.
6. The system checks whether the reported locations fall within the defined matching radius.
7. The system calculates a match probability for compatible items.
8. The system identifies the strongest potential match.
9. The system sends a match notification to the potential owner.

### Alternate Flow
**A1. No suitable match is found**

1. The system compares the newly submitted item against active reports.
2. No item satisfies the required category, color, and location conditions.
3. The system does not generate a match notification.
4. The item report remains active for future matching.
