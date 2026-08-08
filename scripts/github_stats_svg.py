import json
from pathlib import Path


DATA_FILE = Path("assets/github-stats.json")
OUTPUT_FILE = Path("assets/github-stats.svg")


with open(DATA_FILE, "r", encoding="utf-8") as file:
    stats = json.load(file)


username = stats["username"]
repositories = stats["repositories"]
stars = stats["stars"]
contributions = stats["total_contributions"]
commits = stats["commits"]
issues = stats["issues"]
pull_requests = stats["pull_requests"]
current_streak = stats["current_streak"]
longest_streak = stats["longest_streak"]
updated = stats["updated"]


svg = f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="900"
    height="330"
    viewBox="0 0 900 330">

  <style>
    .terminal {{
      font-family: "Courier New", monospace;
    }}

    .label {{
      fill: #8b949e;
      font-size: 14px;
      letter-spacing: 1px;
    }}

    .value {{
      fill: #39d353;
      font-size: 28px;
      font-weight: bold;
    }}

    .small {{
      fill: #8b949e;
      font-size: 12px;
    }}

    .accent {{
      fill: #58a6ff;
    }}
  </style>

  <!-- Background -->
  <rect
    x="1"
    y="1"
    width="898"
    height="328"
    rx="12"
    fill="#0d1117"
    stroke="#30363d"
    stroke-width="2"
  />

  <!-- Terminal header -->
  <circle cx="25" cy="27" r="6" fill="#ff5f56"/>
  <circle cx="45" cy="27" r="6" fill="#ffbd2e"/>
  <circle cx="65" cy="27" r="6" fill="#27c93f"/>

  <text
    x="90"
    y="33"
    class="terminal"
    fill="#8b949e"
    font-size="14">
    {username}@github:~$ git stats
  </text>

  <!-- Divider -->
  <line
    x1="25"
    y1="55"
    x2="875"
    y2="55"
    stroke="#30363d"
  />

  <!-- Main statistics -->

  <text x="95" y="90" class="terminal label">
    CONTRIBUTIONS
  </text>

  <text x="95" y="125" class="terminal value">
    {contributions}
  </text>

  <text x="335" y="90" class="terminal label">
    CURRENT STREAK
  </text>

  <text x="335" y="125" class="terminal value">
    {current_streak} days
  </text>

  <text x="635" y="90" class="terminal label">
    LONGEST STREAK
  </text>

  <text x="635" y="125" class="terminal value">
    {longest_streak} days
  </text>

  <!-- Divider -->
  <line
    x1="25"
    y1="150"
    x2="875"
    y2="150"
    stroke="#30363d"
  />

  <!-- Secondary statistics -->

  <text x="75" y="185" class="terminal label">
    ★ STARS
  </text>

  <text x="75" y="215" class="terminal value">
    {stars}
  </text>


  <text x="245" y="185" class="terminal label">
    COMMITS
  </text>

  <text x="245" y="215" class="terminal value">
    {commits}
  </text>


  <text x="415" y="185" class="terminal label">
    REPOSITORIES
  </text>

  <text x="415" y="215" class="terminal value">
    {repositories}
  </text>


  <text x="615" y="185" class="terminal label">
    ISSUES
  </text>

  <text x="615" y="215" class="terminal value">
    {issues}
  </text>


  <text x="755" y="185" class="terminal label">
    PULL REQS
  </text>

  <text x="755" y="215" class="terminal value">
    {pull_requests}
  </text>

  <!-- Footer -->

  <line
    x1="25"
    y1="245"
    x2="875"
    y2="245"
    stroke="#30363d"
  />

  <text
    x="30"
    y="275"
    class="terminal small">
    last_updated: {updated}
  </text>

  <circle
    cx="785"
    cy="270"
    r="5"
    fill="#39d353"
  />

  <text
    x="800"
    y="275"
    class="terminal small"
    fill="#39d353">
    LIVE
  </text>

</svg>
'''


OUTPUT_FILE.write_text(svg, encoding="utf-8")

print(f"Generated {OUTPUT_FILE}")
