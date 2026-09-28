#!/usr/bin/env python3
"""
Rebuild index.html for the FIRM project page.

All numbers live in this file so the results tables (best / second-best
highlighting included) stay consistent with the paper.  Run:

    python3 build_page.py
"""
import html

# ----------------------------------------------------------------------------
# Table data.  Each row: (label, is_ours, [15 values])
# Column order: Denoising / Deblurring / Super-resolution / Random inpainting /
#               Box inpainting, each as PSNR, SSIM, LPIPS.
# "-" marks a setting where the baseline does not apply.
# ----------------------------------------------------------------------------

TASKS   = ["Denoising", "Deblurring", "Super-resolution", "Random inpainting", "Box inpainting"]
METRICS = [("PSNR", "up"), ("SSIM", "up"), ("LPIPS", "down")]

CELEBA = [
    ("Degraded",     "degraded", [20.00, 0.348, 0.371, 27.81, 0.740, 0.125, 10.25, 0.183, 0.827, 11.95, 0.196, 1.041, 22.26, 0.743, 0.213]),
    ("PnP-GS",       "",         [32.54, 0.908, 0.035, 33.97, 0.924, 0.041, 31.23, 0.890, 0.065, 29.20, 0.875, 0.069, None, None, None]),
    ("PnP-HQS",      "",         [32.17, 0.897, 0.044, 34.87, 0.946, 0.033, 32.33, 0.911, 0.075, 32.81, 0.945, 0.023, None, None, None]),
    ("ISTA-Net",     "",         [None, None, None,    35.38, 0.950, 0.035, 33.54, 0.937, 0.038, 34.70, 0.960, 0.022, None, None, None]),
    ("DiffPIR",      "",         [31.12, 0.883, 0.060, 32.68, 0.910, 0.060, 31.46, 0.893, 0.034, 31.69, 0.916, 0.025, None, None, None]),
    ("I&sup2;SB",    "",         [None, None, None,    33.25, 0.924, 0.012, 31.92, 0.891, 0.014, 32.80, 0.938, 0.011, 28.72, 0.803, 0.042]),
    ("OT-ODE",       "",         [30.49, 0.858, 0.032, 32.96, 0.920, 0.029, 31.34, 0.903, 0.027, 28.65, 0.870, 0.051, 29.37, 0.919, 0.038]),
    ("D-Flow",       "",         [26.01, 0.606, 0.092, 31.21, 0.854, 0.037, 30.44, 0.843, 0.026, 33.61, 0.942, 0.015, 30.59, 0.898, 0.027]),
    ("Flow-Priors",  "",         [29.31, 0.767, 0.135, 31.51, 0.857, 0.056, 28.36, 0.715, 0.100, 32.87, 0.943, 0.019, 30.06, 0.859, 0.048]),
    ("PnP-Flow1",    "",         [31.75, 0.904, 0.044, 34.48, 0.936, 0.039, 31.04, 0.901, 0.045, 33.02, 0.944, 0.018, 30.45, 0.933, 0.037]),
    ("PnP-Flow5",    "",         [32.24, 0.910, 0.056, 34.80, 0.941, 0.046, 31.44, 0.905, 0.056, 33.95, 0.953, 0.022, 31.06, 0.939, 0.043]),
    ("Flower1-OT",   "",         [32.22, 0.913, 0.033, 34.95, 0.947, 0.025, 32.30, 0.922, 0.034, 33.05, 0.944, 0.017, 31.17, 0.945, 0.022]),
    ("Flower5-OT",   "",         [33.07, 0.925, 0.038, 35.65, 0.954, 0.031, 33.03, 0.931, 0.039, 33.92, 0.953, 0.020, 31.85, 0.952, 0.023]),
    ("Ours (N=2)",   "ours",     [33.67, 0.932, 0.034, 36.04, 0.957, 0.029, 34.39, 0.949, 0.028, 35.03, 0.963, 0.018, 33.25, 0.960, 0.022]),
    ("Ours (N=4)",   "ours",     [33.24, 0.928, 0.034, 35.78, 0.956, 0.028, 33.96, 0.946, 0.026, 34.67, 0.962, 0.016, 32.57, 0.958, 0.021]),
    ("Ours (N=10)",  "ours",     [32.26, 0.914, 0.032, 35.03, 0.950, 0.023, 33.13, 0.937, 0.022, 33.98, 0.956, 0.014, 31.85, 0.953, 0.020]),
    ("Ours (N=25)",  "ours",     [31.56, 0.901, 0.028, 31.46, 0.848, 0.026, 30.39, 0.837, 0.029, 33.42, 0.951, 0.013, 31.33, 0.947, 0.020]),
]

AFHQ = [
    ("Degraded",     "degraded", [20.00, 0.293, 0.529, 24.38, 0.529, 0.436, 11.59, 0.212, 0.867, 13.23, 0.213, 1.082, 21.52, 0.727, 0.215]),
    ("PnP-GS",       "",         [33.00, 0.895, 0.078, 28.39, 0.787, 0.387, 24.44, 0.639, 0.411, 29.82, 0.844, 0.143, None, None, None]),
    ("PnP-HQS",      "",         [32.69, 0.896, 0.108, 29.34, 0.793, 0.362, 26.58, 0.724, 0.441, 33.07, 0.916, 0.051, None, None, None]),
    ("ISTA-Net",     "",         [None, None, None,    29.36, 0.790, 0.342, 28.22, 0.784, 0.297, 34.10, 0.929, 0.049, None, None, None]),
    ("DiffPIR",      "",         [31.05, 0.839, 0.186, 28.24, 0.747, 0.319, 24.24, 0.650, 0.385, 32.31, 0.886, 0.057, None, None, None]),
    ("I&sup2;SB",    "",         [None, None, None,    27.72, 0.725, 0.077, 27.19, 0.739, 0.070, 31.79, 0.879, 0.026, 27.32, 0.763, 0.072]),
    ("OT-ODE",       "",         [30.48, 0.818, 0.081, 27.82, 0.735, 0.126, 26.71, 0.737, 0.108, 29.99, 0.849, 0.087, 24.47, 0.873, 0.095]),
    ("D-Flow",       "",         [26.44, 0.573, 0.180, 28.60, 0.746, 0.167, 25.20, 0.616, 0.188, 32.79, 0.898, 0.044, 27.02, 0.840, 0.081]),
    ("Flow-Priors",  "",         [29.67, 0.756, 0.165, 27.28, 0.726, 0.188, 23.95, 0.566, 0.274, 32.95, 0.909, 0.051, 26.13, 0.809, 0.130]),
    ("PnP-Flow1",    "",         [31.62, 0.866, 0.139, 28.71, 0.779, 0.285, 27.56, 0.780, 0.158, 33.71, 0.923, 0.038, 26.45, 0.895, 0.111]),
    ("PnP-Flow5",    "",         [31.87, 0.868, 0.170, 29.01, 0.785, 0.312, 28.01, 0.791, 0.167, 34.44, 0.932, 0.045, 27.14, 0.900, 0.127]),
    ("Flower1-OT",   "",         [32.12, 0.881, 0.113, 29.38, 0.793, 0.237, 26.76, 0.759, 0.262, 33.68, 0.922, 0.042, 26.67, 0.914, 0.065]),
    ("Flower5-OT",   "",         [32.75, 0.892, 0.126, 29.73, 0.801, 0.264, 27.09, 0.767, 0.272, 34.36, 0.931, 0.048, 27.32, 0.922, 0.067]),
    ("Ours (N=2)",   "ours",     [33.31, 0.904, 0.081, 29.89, 0.809, 0.229, 29.10, 0.816, 0.167, 34.71, 0.936, 0.043, 29.27, 0.924, 0.060]),
    ("Ours (N=4)",   "ours",     [32.93, 0.898, 0.079, 29.42, 0.796, 0.188, 28.50, 0.801, 0.141, 34.30, 0.932, 0.039, 28.65, 0.921, 0.052]),
    ("Ours (N=10)",  "ours",     [31.96, 0.879, 0.072, 28.72, 0.775, 0.145, 27.75, 0.777, 0.115, 33.53, 0.922, 0.033, 27.94, 0.916, 0.047]),
    ("Ours (N=25)",  "ours",     [29.69, 0.776, 0.081, 28.16, 0.754, 0.119, 26.54, 0.676, 0.121, 32.91, 0.912, 0.030, 26.76, 0.819, 0.077]),
]


def fmt(v, metric):
    if v is None:
        return "&ndash;"
    return f"{v:.2f}" if metric == "PSNR" else f"{v:.3f}"


def big_table(rows):
    """Render a 5-task x 3-metric results table with best/second-best marks."""
    ncol = len(TASKS) * len(METRICS)

    # rank each column, ignoring the Degraded reference row
    marks = [dict() for _ in range(ncol)]
    for c in range(ncol):
        _, direction = METRICS[c % 3]
        vals = [(r[2][c], i) for i, r in enumerate(rows)
                if r[1] != "degraded" and r[2][c] is not None]
        vals.sort(key=lambda t: t[0], reverse=(direction == "up"))
        if len(vals) > 0:
            marks[c][vals[0][1]] = "best"
        if len(vals) > 1 and vals[1][0] != vals[0][0]:
            marks[c][vals[1][1]] = "second"
        elif len(vals) > 1:                     # tie for first -> both best
            marks[c][vals[1][1]] = "best"

    out = ['<table class="results">', "<thead>"]
    out.append('<tr class="groups"><th></th>' +
               "".join(f'<th colspan="3">{t}</th>' for t in TASKS) + "</tr>")
    arrows = {"PSNR": "&uarr;", "SSIM": "&uarr;", "LPIPS": "&darr;"}
    out.append('<tr class="metrics"><th>Method</th>' +
               "".join(f"<th>{m}{arrows[m]}</th>" for _ in TASKS for m, _ in METRICS) + "</tr>")
    out.append("</thead><tbody>")

    for i, (label, cls, vals) in enumerate(rows):
        classes = [c for c in (cls,) if c]
        if label.startswith("Ours") and not rows[i - 1][0].startswith("Ours"):
            classes.append("sep-top")
        if i == 1:
            classes.append("sep-top")
        tr = f' class="{" ".join(classes)}"' if classes else ""
        cells = []
        for c, v in enumerate(vals):
            mark = marks[c].get(i, "")
            td = f' class="{mark}"' if mark else ""
            cells.append(f"<td{td}>{fmt(v, METRICS[c % 3][0])}</td>")
        out.append(f"<tr{tr}><td>{label}</td>" + "".join(cells) + "</tr>")

    out.append("</tbody></table>")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Cost table (Table 3)
# ----------------------------------------------------------------------------

COST_METHODS = ["OT-ODE", "D-Flow", "Flow&nbsp;Priors", "PnP-Flow1", "PnP-Flow5",
                "Flower1", "Flower5", "Ours (N=2)", "Ours (N=4)", "Ours (N=10)", "Ours (N=25)"]
COST_TIME = [6.37, 299.25, 41.27, 2.33, 11.46, 2.67, 13.03, 0.24, 0.50, 1.21, 3.13]
COST_MEM  = [743, 6124, 2728, 192, 192, 193, 193, 331, 331, 331, 331]
COST_NFE  = [180, None, 100, 100, 500, 100, 500, 10, 20, 50, 125]


def cost_table():
    def rank(vals, skip=()):
        pairs = sorted([(v, i) for i, v in enumerate(vals) if v is not None and i not in skip])
        m = {}
        if pairs:
            m[pairs[0][1]] = "best"
        for v, i in pairs[1:]:
            if v == pairs[0][0]:
                m[i] = "best"
            else:
                m[i] = "second"
                break
        return m

    mt, mm, mn = rank(COST_TIME), rank(COST_MEM), rank(COST_NFE)

    def row(name, vals, marks, fmt_fn):
        cells = []
        for i, v in enumerate(vals):
            cls = marks.get(i, "")
            td = f' class="{cls}"' if cls else ""
            cells.append(f"<td{td}>{fmt_fn(v) if v is not None else '&ndash;'}</td>")
        return f"<tr><td>{name}</td>" + "".join(cells) + "</tr>"

    head = ('<table class="results compact"><thead>'
            '<tr class="metrics"><th>Metric</th>' +
            "".join(f"<th>{m}</th>" for m in COST_METHODS) + "</tr></thead><tbody>")
    body = (row("Time (s) &darr;",        COST_TIME, mt, lambda v: f"{v:.2f}") +
            row("Peak memory (MB) &darr;", COST_MEM,  mm, lambda v: f"{v:,}") +
            row("NFEs &darr;",             COST_NFE,  mn, lambda v: f"{v}"))
    return head + body + "</tbody></table>"


def simple_table(headers, rows, compact=True):
    cls = "results compact" if compact else "results"
    out = [f'<table class="{cls}"><thead><tr class="metrics">']
    out += [f"<th>{h}</th>" for h in headers]
    out.append("</tr></thead><tbody>")
    for r in rows:
        tr = ' class="ours"' if r[0].startswith("Ours") else ""
        out.append(f"<tr{tr}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


ABL_K = simple_table(
    ["K", "PSNR &uarr;", "SSIM &uarr;", "LPIPS &darr;", "Time (ms) &darr;"],
    [["3", "34.63", "0.959", "0.020", "137"],
     ["<b>5</b>", "<b>35.03</b>", "<b>0.963</b>", "<b>0.018</b>", "<b>223</b>"],
     ["7", "35.21", "0.964", "0.019", "322"]])

ABL_NOISE = simple_table(
    ["Method", "&sigma;<sub>test</sub>=0.005 &middot; PSNR &uarr;", "SSIM &uarr;", "LPIPS &darr;",
     "&sigma;<sub>test</sub>=0.02 &middot; PSNR &uarr;", "SSIM &uarr;", "LPIPS &darr;"],
    [["Flower5-OT", "34.02", "0.954", "0.019", "33.65", "0.947", "0.024"],
     ["Ours", "<b>35.19</b>", "<b>0.965</b>", "<b>0.018</b>", "<b>34.57</b>", "<b>0.954</b>", "<b>0.020</b>"]])

ABL_MASK = simple_table(
    ["Test mask ratio p", "PSNR &uarr;", "SSIM &uarr;", "LPIPS &darr;"],
    [["0.5", "38.26", "0.978", "0.008"],
     ["0.6", "36.95", "0.973", "0.012"],
     ["0.7 &dagger; <span class='muted'>(training ratio)</span>", "35.03", "0.963", "0.018"],
     ["0.8", "32.10", "0.936", "0.034"]])

# ----------------------------------------------------------------------------

with open("template.html", encoding="utf-8") as f:
    page = f.read()

page = (page
        .replace("<!--TABLE_CELEBA-->", big_table(CELEBA))
        .replace("<!--TABLE_AFHQ-->",   big_table(AFHQ))
        .replace("<!--TABLE_COST-->",   cost_table())
        .replace("<!--TABLE_K-->",      ABL_K)
        .replace("<!--TABLE_NOISE-->",  ABL_NOISE)
        .replace("<!--TABLE_MASK-->",   ABL_MASK))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page)

print("index.html written ({:,} bytes)".format(len(page)))
