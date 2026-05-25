Two Feature Suggestions

  1. Salary Revision History (Salary Management)

  Add a SalaryRevision model that creates an audit record whenever an employee's salary
  changes — storing old_salary, new_salary, effective_date, and reason. Add an endpoint GET
   /api/employees/{id}/salary-history/ that returns the full revision log.

  Why it's good for TDD:
  The red cycle is clear and layered — you write tests for model creation, then for the
  signal/override that auto-creates revisions, then for the API endpoint, then for edge
  cases (first salary isn't a "revision", inactive employee still has history). Each test
  drives one small implementation step.

  ---
  2. Salary Recommendation Agent (Agentic AI)
  
  Add a POST /api/employees/recommend-salary/ endpoint that accepts { job_title, country, 
  description } and uses Claude with tool use to produce a salary recommendation. Claude
  gets one tool: query_salary_stats(job_title, country) which hits your existing insights
  logic. The agent calls the tool, gets real data from your DB, and synthesizes a
  recommended range with reasoning.

  Why it's genuinely agentic:
  It's not just a prompt — it's a tool-use loop where Claude decides when to call your DB
  query, interprets the result, and produces a grounded answer. You'll test: the tool
  invocation is triggered when data is missing, the tool result feeds back into the
  response, the final output contains a numeric range, and the endpoint handles the case
  where no comparable data exists (Claude should say so rather than hallucinate).

  Why it's good for TDD:
  You can mock the Anthropic client at the boundary
  (unittest.mock.patch("anthropic.Anthropic")), write failing tests for each step of the
  agent loop, then implement. The mock-vs-real DB distinction is clear: the DB calls are
  real (per your project rule), only the LLM call is mocked.