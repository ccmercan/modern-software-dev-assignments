# Test Inputs for Action Item Extractor

Copy and paste these into the textarea to test different extraction scenarios.

## Test 1: Basic Bullet Points and Checkboxes
```
Meeting notes from today:
- [ ] Set up the database connection
* Implement the API extract endpoint
1. Write unit tests for the new feature
2. Update the documentation
Some regular narrative text that should be ignored.
```

## Test 2: Keyword Prefixes
```
Weekly standup notes:
todo: Review the pull requests
action: Fix the authentication bug
next: Deploy to staging environment
action: Schedule the team meeting
Regular discussion about project status.
```

## Test 3: Imperative Sentences
```
During our sprint planning meeting we discussed:
Create a new user authentication system.
Update the API documentation with latest changes.
Fix the login bug that's blocking production.
Refactor the database queries for better performance.
We also talked about the upcoming release.
```

## Test 4: Mixed Formats (Complex)
```
Team Meeting - January 15, 2024

Updates:
John mentioned the database migration is complete.
Sarah is working on the frontend redesign.

Action Items:
- [ ] Fix the authentication bug reported by QA team
* Implement rate limiting for API endpoints
1. Write integration tests for payment module
todo: Update deployment documentation
action: Schedule security audit for next month
next: Review and merge pending pull requests

We need to prioritize the authentication fix as it's blocking deployment.
The team will reconvene next week to review progress.
```

## Test 5: Nested and Complex Structure
```
Project Planning Session:

Main Tasks:
- Main task: Implement user authentication
  - Sub-task: Create login page UI
  - Sub-task: Add password reset functionality
  - Sub-task: Implement two-factor authentication
* Another main task: Optimize database queries
  1. Analyze slow queries
  2. Add proper indexes
  3. Update query patterns

Additional items:
todo: Set up CI/CD pipeline
action: Write API documentation
next: Deploy to production server
```

## Test 6: Minimal Input (Edge Case)
```
todo: Complete the project
```

## Test 7: No Action Items (Should Return Empty)
```
This is just a regular paragraph with no action items.
It contains some narrative text about a meeting.
Everyone discussed various topics but no tasks were assigned.
The conversation was mostly about planning and strategy.
```

## Test 8: Real-World Meeting Notes
```
Sprint Retrospective - Week 2

What went well:
- Team collaboration improved
- Code review process is working smoothly

What needs improvement:
- [ ] Reduce deployment time
- [ ] Improve test coverage
* Add more logging for debugging
1. Update error messages to be more user-friendly

Action items for next sprint:
todo: Research new deployment tools
action: Set up automated testing pipeline
next: Schedule training session for new team members
action: Review and update documentation

Next steps:
We'll start implementing these improvements in the next sprint.
```

## Testing Instructions:

1. **Test Heuristic Extraction:**
   - Paste any test input above
   - Click "Extract" button
   - Check if action items are extracted correctly

2. **Test LLM Extraction:**
   - Paste the same test input
   - Click "Extract LLM" button
   - Compare results with heuristic extraction
   - Note: LLM extraction may take 10-20 seconds

3. **Test Save Note:**
   - Check "Save as note" checkbox
   - Extract items (either method)
   - Click "List Notes" to see saved notes

4. **Test List Notes:**
   - Click "List Notes" button
   - Should display all previously saved notes

5. **Test Action Item Checkboxes:**
   - After extraction, check/uncheck items
   - Status should be saved to database

## Expected Results:

- **Test 1-5:** Should extract multiple action items
- **Test 6:** Should extract 1 action item
- **Test 7:** Should return "No action items found"
- **Test 8:** Should extract all actionable items

## Comparison Test:

Try the same input with both "Extract" and "Extract LLM" to see differences:
- Heuristic: Fast, rule-based, may miss some items
- LLM: Slower, more intelligent, may catch items heuristic misses
