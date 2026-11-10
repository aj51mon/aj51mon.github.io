from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo

wb = Workbook()
F = "Arial"
hdr_font = Font(name=F, bold=True, color="FFFFFF")
hdr_fill = PatternFill("solid", fgColor="1F4E78")
body = Font(name=F, size=10)
wrap = Alignment(wrap_text=True, vertical="top")

def build(ws, headers, rows, widths, name):
    ws.append(headers)
    for r in rows: ws.append(r)
    for c in ws[1]:
        c.font = hdr_font; c.fill = hdr_fill
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = body; c.alignment = wrap
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65+i)].width = w
    ref = f"A1:{chr(64+len(headers))}{len(rows)+1}"
    t = Table(displayName=name, ref=ref)
    t.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
    ws.add_table(t)
    ws.freeze_panes = "B2"
    ws.row_dimensions[1].height = 30

lib = wb.active; lib.title = "Exercise Library"
lib_h = ["Exercise","Primary body group","Secondary muscles","Workout categories","Sets","Reps / duration","Equipment","Notes","Workout reference"]
lib_r = [
 ["Jump Squats","Legs","Quadriceps, Glutes","Plyometrics, Power / Explosiveness, Bilateral, Legs / Lower Body",3,"5 reps","","","W001"],
 ["Single-Leg Hops","Legs","Calves, Quadriceps","Plyometrics, Reactive Strength, Unilateral, Legs / Lower Body",3,"15 seconds per leg","","","W001"],
 ["Pogo Hops","Calves","Quadriceps","Plyometrics, Reactive Strength, Bilateral, Legs / Lower Body",3,"30 seconds","","","W001"],
 ["Split Squat Jumps","Legs","Quadriceps, Glutes","Plyometrics, Power / Explosiveness, Split-Stance, Legs / Lower Body",3,"15 seconds","","Unclear if per leg or alternating; kept as given","W001"],
 ["Running in Place / High Knees","Legs","Hip flexors, Calves","Conditioning, Legs / Lower Body",3,"30 seconds","","Logged as one entry; split if a source separates them","W001"],
 ["Skater Jumps","Glutes","Quadriceps","Plyometrics, Lateral Movement, Unilateral, Legs / Lower Body",3,"20 seconds","","","W001"],
 ["Jumping Jacks","Full Body","Calves, Shoulders","Conditioning, Plyometrics, Full Body",3,"30 seconds","","","W001"],
 ["Vertical Jumps","Legs","Quadriceps, Glutes, Calves","Plyometrics, Power / Explosiveness, Bilateral, Legs / Lower Body","","15 reps","","Primes nervous system; best jump 30.1 in noted in video; sets not stated","W002"],
 ["Back Squats","Legs","Quadriceps, Glutes","Strength, Bilateral, Legs / Lower Body","1 + 3","1 x 5 reps @ 85% 1RM, then 3 x 6-8 reps @ 80% 1RM","Barbell, power rack","Main strength lift; block accumulating reps in 5-8 range","W002"],
 ["Barbell Romanian Deadlifts (RDLs)","Legs","Hamstrings, Glutes","Strength, Pull, Bilateral, Legs / Lower Body",3,"6-8 reps","Barbell; lifting belt + straps recommended for heavy loads","Push hips back, lower to mid-shin","W002"],
 ["Dumbbell Walking Lunges","Legs","Quadriceps, Glutes","Strength, Unilateral, Balance / Stability, Legs / Lower Body",2,"6 reps per leg","Dumbbells (100 lb used)","","W002"],
 ["Nordic Ham Curls (band-assisted)","Legs","Hamstrings","Strength, Rehab / Prehab, Bilateral, Legs / Lower Body",2,"6 reps","Resistance band","Band assists controlled eccentric; used in place of hamstring curl machine","W002"],
 ["Barbell Bench Press","Chest","Anterior deltoids, Triceps","Push, Strength, Hypertrophy, Bilateral, Upper Body","3-4","6-10 reps","","Flat press slot. Swaps: dumbbell bench, machine chest press. Rest 90-120 s","W003"],
 ["Pull-Ups","Back","Lats, Upper back, Biceps","Pull, Strength, Hypertrophy, Upper Body","3-4","8-12 reps","","Overhead pull slot. Swaps: assisted pull-ups, machine or cable lat pulldown. Rest 90-120 s","W003"],
 ["Incline Barbell Press","Chest","Upper chest, Anterior deltoids, Triceps","Push, Strength, Hypertrophy, Upper Body","3-4","8-12 reps","","Incline press slot. Swaps: incline dumbbell, incline machine press. Rest 90-120 s","W003"],
 ["T-Bar Row","Back","Mid-back, Rear deltoids, Rhomboids","Pull, Strength, Hypertrophy, Upper Body","3-4","8-12 reps","","Row slot. Swaps: one-arm DB row, seated cable row, bent-over barbell row. Rest 90-120 s","W003"],
 ["Dumbbell Lateral Raise","Shoulders","Lateral deltoids","Hypertrophy, Upper Body",3,"12-15 reps","","Side delt slot. Swaps: machine or cable lateral raise. Rest 60-90 s","W003"],
 ["Dumbbell Curl","Arms","Biceps","Pull, Hypertrophy, Upper Body",3,"10-15 reps","","Bicep slot. Swaps: barbell, cable or machine curl. Rest 60-90 s","W003"],
 ["Cable Tricep Pushdown","Arms","Triceps","Push, Hypertrophy, Upper Body",3,"10-15 reps","","Tricep slot. Swaps: rope pushdown, overhead DB extension, machine extension. Rest 60-90 s","W003"],
]

idx = wb.create_sheet("Workout Index")
idx_h = ["Workout ID","Workout name","Primary category","Secondary categories","#","Exercise","Sets","Reps / duration"]
idx_r = [["W001","Lower-Body Plyometrics","Plyometrics","Legs / Lower Body",i+1,r[0],r[4],r[5]] for i,r in enumerate(lib_r[:7])]
idx_r += [["W002","Heavy Leg Day: Power + Strength","Strength","Power / Explosiveness, Legs / Lower Body",i+1,r[0],r[4],r[5]] for i,r in enumerate(lib_r[7:12])]
idx_r += [["W003","Full Upper Body","Hypertrophy","Strength, Upper Body, Push, Pull",i+1,r[0],r[4],r[5]] for i,r in enumerate(lib_r[12:19])]
# ---- Aaron's Monday-Friday programme (designed 3 Nov 2026 from logged data, 14 Oct - 2 Nov) ----
# (exercise, sets, reps/load, body, secondary, tags, equipment, notes)
PROGRAM = [
 ("W004","Monday: Upper Strength","Strength","Upper Body, Push, Pull, Hypertrophy",[
  ("Barbell Bench Press","4","4 @ 85 kg","Chest","Anterior deltoids, Triceps","Push, Strength, Bilateral, Upper Body","Barbell, bench","Heavy bench day. Add 2.5 kg when all 4 sets of 4 are clean. No singles until the re-test"),
  ("Lat Pulldown","4","6-8 @ 70 kg","Back","Lats, Biceps","Pull, Strength, Upper Body","Cable stack","Last best 66 x 10"),
  ("Seated Barbell Overhead Press","3","5 @ 50 kg","Shoulders","Triceps","Push, Strength, Upper Body","Barbell, bench","Add 2.5 kg once 3 x 5 is clean"),
  ("Low row","3","8 @ 60 kg","Back","Mid-back, Biceps","Pull, Strength, Upper Body","Row machine","Last best 60 x 8, 8, 6"),
  ("Tricep Pushdown","3","10-12 @ 18 kg","Arms","Triceps","Push, Hypertrophy, Upper Body","Cable","Keep every set at 10+ reps; add weight only then"),
  ("Face Pull","3","12-15","Shoulders","Rear deltoids, Upper back","Pull, Hypertrophy, Rehab / Prehab, Upper Body","Cable, rope","Light. Shoulder and elbow health"),
 ]),
 ("W005","Tuesday: Lower Strength + Power","Strength","Power / Explosiveness, Legs / Lower Body",[
  ("Box Jump","3","3","Legs","Glutes, Calves","Plyometrics, Power / Explosiveness, Bilateral, Legs / Lower Body","Plyo box","First, fresh. Full rest. Step down, don't jump down"),
  ("Back Squat","3","5 @ 102.5 kg","Legs","Quadriceps, Glutes","Strength, Bilateral, Legs / Lower Body","Barbell, rack","Add 2.5 kg per session while reps stay clean. Elbow sore? Swap to Belt Squat or Safety Bar Squat"),
  ("Romanian Deadlift","3","6-8 @ 60 kg","Legs","Hamstrings, Glutes, Lower back","Strength, Pull, Bilateral, Legs / Lower Body","Barbell","New. Hips back, bar close, lower to mid-shin"),
  ("Belt Squat","2","10 @ 120 kg","Legs","Quadriceps, Glutes","Hypertrophy, Bilateral, Legs / Lower Body","Belt squat machine","Elbow-free quad volume. Last best 130 x 10"),
  ("Lying Leg Curl","3","10-12","Legs","Hamstrings","Hypertrophy, Legs / Lower Body","Machine","New. Pick a weight that leaves 1-2 reps in reserve"),
  ("Standing Calf Raise","3","12-15","Calves","","Hypertrophy, Legs / Lower Body","Machine","Pause at the bottom"),
 ]),
 ("W006","Wednesday: Aerobic Base + Core","Conditioning","Mobility, Full Body",[
  ("Weighted Crunch","3","8-10 @ 40 kg","Core","Abdominals","Strength, Hypertrophy","Cable or machine","Last best 43 x 9"),
  ("Hanging Knee Raise","3","10-12","Core","Hip flexors, Abdominals","Hypertrophy, Balance / Stability","Pull-up bar",""),
  ("Farmer's Carry","3","30-40 m","Full Body","Forearms, Core, Traps","Conditioning, Strength, Balance / Stability","Dumbbells or handles","Heavy but upright"),
 ]),
 ("W007","Thursday: Upper Volume","Hypertrophy","Upper Body, Push, Pull, Strength",[
  ("Barbell Bench Press","3","8 @ 72.5 kg","Chest","Anterior deltoids, Triceps","Push, Hypertrophy, Bilateral, Upper Body","Barbell, bench","Volume bench day. Add 2.5 kg once all 3 sets reach 8"),
  ("Seated row","4","8-10 @ 55 kg","Back","Mid-back, Biceps","Pull, Hypertrophy, Upper Body","Cable","Last best 53 x 12"),
  ("Lat Pulldown","3","10-12 @ 59 kg","Back","Lats, Biceps","Pull, Hypertrophy, Upper Body","Cable stack",""),
  ("Incline Dumbbell Press","3","8-10 @ 25 kg/hand","Chest","Upper chest, Anterior deltoids, Triceps","Push, Hypertrophy, Upper Body","Dumbbells, incline bench","Last best 25 x 10 per hand"),
  ("Dumbbell Lateral Raise","3","12-15","Shoulders","Lateral deltoids","Hypertrophy, Upper Body","Dumbbells",""),
  ("Dumbbell Curl","3","10-12 @ 15 kg/hand","Arms","Biceps","Pull, Hypertrophy, Upper Body","Dumbbells","Stuck at 15 x 10 for 5 sessions. Get 3 x 12, then 17.5 kg"),
  ("Rope Pushdown","2","12 @ 22 kg","Arms","Triceps","Push, Hypertrophy, Upper Body","Cable, rope",""),
 ]),
 ("W008","Friday: Lower Power + Hypertrophy","Power / Explosiveness","Hypertrophy, Legs / Lower Body",[
  ("Hang Power Clean","5","3 @ 45 kg","Full Body","Hamstrings, Glutes, Traps","Power / Explosiveness, Plyometrics, Full Body","Barbell","First, fresh. Fast reps; stop the set if speed drops. See Coaching cues"),
  ("Belt Squat","3","8-10 @ 130 kg","Legs","Quadriceps, Glutes","Strength, Hypertrophy, Bilateral, Legs / Lower Body","Belt squat machine","Heavy quad work without loading the elbow"),
  ("Bulgarian Split Squat","3","8 per leg","Legs","Quadriceps, Glutes","Hypertrophy, Unilateral, Balance / Stability, Legs / Lower Body","Dumbbells","New. Start with bodyweight or light dumbbells"),
  ("Seated Leg Curl","3","10-12","Legs","Hamstrings","Hypertrophy, Legs / Lower Body","Machine","New"),
  ("Leg extensions","3","12 @ 55 kg","Legs","Quadriceps","Hypertrophy, Legs / Lower Body","Machine","Last best 63 x 10"),
 ]),
]
names = [r[0] for r in lib_r]
for wid, wname, prim, sec, items in PROGRAM:
    for k, (ex, sets, reps, body, secm, tags, eq, notes) in enumerate(items):
        if ex in names:
            r = lib_r[names.index(ex)]; r[8] = r[8] + ", " + wid
        else:
            lib_r.append([ex, body, secm, tags, sets, reps, eq, notes, wid]); names.append(ex)
        idx_r.append([wid, wname, prim, sec, k+1, ex, sets, reps])

build(lib, lib_h, lib_r, [28,16,22,44,7,18,12,36,12], "ExerciseLibrary")
build(idx, idx_h, idx_r, [11,24,16,20,5,28,7,18], "WorkoutIndex")
for row in idx.iter_rows(min_row=2):
    row[4].alignment = Alignment(horizontal="center", vertical="top")


cc = wb.create_sheet("Coaching Cues")
M = "Hang Power Clean"
cues = [
 ("1. Setup & Safety","Start with an empty bar; master the pattern before loading."),
 ("1. Setup & Safety","Feet hip-width, bar at mid-thigh (hang)."),
 ("1. Setup & Safety","Shoulders slightly ahead of bar, lats engaged, core braced, neutral spine."),
 ("2. Mobility & Grip","Elbow reaches: alternate each elbow up and back to open lats/shoulders. Prevents low-elbow catch."),
 ("2. Mobility & Grip","Hook grip: thumb on bar first, index + middle fingers over thumb."),
 ("2. Mobility & Grip","Hook grip feels awkward at first; re-grip it on every descent until habitual."),
 ("3. Hip Muscle Clean (shrug + pull)","From hang, drive legs and hips into a vertical shrug."),
 ("3. Hip Muscle Clean (shrug + pull)","Keep bar close; punch elbows up and high, like the top of a hammer curl."),
 ("3. Hip Muscle Clean (shrug + pull)","Release hook at the top, re-catch on the way down."),
 ("3. Hip Muscle Clean (shrug + pull)","Goal: speed and height in the upper pull, no knee re-bend."),
 ("4. Hang Muscle Clean (hip-knee-hip)","Hip: hinge, knees slightly bent."),
 ("4. Hang Muscle Clean (hip-knee-hip)","Knee: load hamstrings, slight knee re-bend to build posterior-chain tension."),
 ("4. Hang Muscle Clean (hip-knee-hip)","Hip: drive back through, then explode into shrug, pull, elbows high."),
 ("4. Hang Muscle Clean (hip-knee-hip)","Think: kettlebell-swing hinge + hammer curl finish."),
 ("5. Full Hang Power Clean","Start in hang: hips back, knees bent, bar at mid-thigh."),
 ("5. Full Hang Power Clean","First pull to power position: hip, knee, hip. Bar stays close."),
 ("5. Full Hang Power Clean","Triple extension: jump vertically through ankles, knees and hips together. Legs make the height, not arms."),
 ("5. Full Hang Power Clean","As you leave the ground, shrug hard and pull, bar tight to torso."),
 ("5. Full Hang Power Clean","Catch: elbows up and around fast; knees out, hips back into a partial squat."),
 ("5. Full Hang Power Clean","Receive on front rack with elbows high and torso upright, not collapsed."),
 ("5. Full Hang Power Clean","Stand tall, reset feet if needed, lower to hang under control."),
 ("6. Key Cues","Bar path: straight vertical line, close to the body."),
 ("6. Key Cues","Hip-knee-hip sets the timing for the second pull."),
 ("6. Key Cues","Jump makes height, shrug starts the pull, pull brings the bar up."),
 ("6. Key Cues","Receive, don't chase: drive the bar up, then get under it. No arm-pulling, no low elbows."),
 ("7. Progression","Start 3 x 10 light to build the pattern."),
 ("7. Progression","When confident, add load and drop reps."),
 ("7. Progression","As load rises it becomes a squat clean: if the bar won't go high enough, drop into a full front squat to receive."),
 ("8. Common Errors","Low elbows on catch: elbow mobility drills + drive elbows high."),
 ("8. Common Errors","Knees shooting forward: hips back first, then slight knee bend. Avoid the knee jut."),
 ("9. Principle","Legs and hips drive the clean; arms are just hooks to guide and receive."),
 ("9. Principle","Every session: empty bar first to groove the pattern."),
]
cc_r = [[M, sec, i+1, cue] for i,(sec,cue) in enumerate(cues)]
ub = [
 ("1. Structure","4 compounds, then 3 isolations."),
 ("1. Structure","Any exercise with the same movement pattern can be swapped in (see each exercise's notes)."),
 ("2. Order","Compounds first while fresh; isolations last."),
 ("3. Load & Progression","Start with a weight that leaves 1-2 reps in reserve."),
 ("3. Load & Progression","Add weight or reps weekly while form holds."),
 ("4. Tempo","Control the lowering phase on every rep."),
 ("5. Rest","Compounds: 90-120 s between sets."),
 ("5. Rest","Isolations: 60-90 s between sets."),
 ("6. Frequency","2x per week, or within a push/pull or upper/lower split."),
 ("7. Principle","Consistency and progressive overload over exercise variety."),
 ("7. Principle","Balanced push and pull protects shoulder health and posture."),
]
cc_r += [["Full Upper Body", sec, i+1, cue] for i,(sec,cue) in enumerate(ub)]
WEEK = [
 ("1. The week","Mon upper strength, Tue lower strength + power, Wed aerobic + core, Thu upper volume, Fri lower power + size. Sat/Sun rest or an easy walk, ride or swim."),
 ("1. The week","Bench twice (heavy Mon, volume Thu), legs twice, hamstrings twice, about 10 direct arm sets a week."),
 ("2. Progression","Loads in each plan come from your logged sets. When every set hits the top of the rep range, add 2.5 kg (1-2 kg per hand on dumbbells)."),
 ("2. Progression","Miss the reps two sessions running? Drop 5% and build back."),
 ("2. Progression","Every 5th week: same exercises, about half the sets, to recover."),
 ("2. Progression","Re-test bench and squat singles after 4 weeks, not before."),
 ("3. Order","Jumps and cleans first while fresh, then the heavy lift, then accessories. Rest timer: 2-3 min on main lifts, 60-90 s on isolations."),
 ("4. Cardio","Wednesday: 35-40 min easy (bike, row or run) at a pace you could talk through. Log heart rate."),
 ("4. Cardio","Friday: 20-30 min easy after lifting, or on the weekend. Keep your row/ski time trials to one a week, on Monday."),
 ("5. Elbow","If squatting with the bar hurts the elbow, swap Back Squat for Belt Squat or Safety Bar Squat that day. Wide, thumbless grip otherwise."),
 ("6. Tracking","Start each day from its plan so sessions compare week to week. Weigh in 3-4 mornings a week."),
]
TODAY = {
 "Monday: Upper Strength": "Heavy bench day. Quality reps, full rest (2-3 min) on bench, pulldown and press. Finish with your 2 km row time trial if you have energy.",
 "Tuesday: Lower Strength + Power": "Jump fresh, then squat. RDL is new: find a weight that leaves 2 reps in the tank. If the elbow complains, belt squat instead of back squat.",
 "Wednesday: Aerobic Base + Core": "Easy day. 35-40 min of cardio at a pace you could talk through (tap + Add cardio), then the core circuit. Nothing should feel hard.",
 "Thursday: Upper Volume": "Volume day. Steady reps, 60-90 s rest on the accessories. Curls: chase 3 x 12 before going heavier.",
 "Friday: Lower Power + Hypertrophy": "Cleans first, fast and crisp: end the set if the bar slows. Then legs. Finish with 20-30 min easy cardio.",
}
cc_r += [[nm, "0. Today", 1, txt] for nm, txt in TODAY.items()]
cc_r += [["Monday: Upper Strength", sec, i+1, cue] for i,(sec,cue) in enumerate(WEEK)]
for nm in ["Tuesday: Lower Strength + Power","Wednesday: Aerobic Base + Core","Thursday: Upper Volume","Friday: Lower Power + Hypertrophy"]:
    cc_r.append([nm, "1. Programme", 1, "Part of your Monday-Friday programme. Full rules are under Monday: Upper Strength → Guidelines."])
WED_EXTRA = [("2. Today","Do 35-40 min of easy cardio first or after the core work: tap + Add cardio in the workout and log it there."),("2. Today","Easy means nose-breathing or full sentences. If you've set your max HR, aim for Zone 2.")]
cc_r += [["Wednesday: Aerobic Base + Core", s2, i+2, c2] for i,(s2,c2) in enumerate(WED_EXTRA)]
build(cc, ["Movement","Section","#","Cue"], cc_r, [18,30,5,70], "CoachingCues")
for row in cc.iter_rows(min_row=2):
    row[2].alignment = Alignment(horizontal="center", vertical="top")

wb.save("Workout_Exercise_Library.xlsx")

import json
wk = {}
for r in idx_r:
    w = wk.setdefault(r[0], {"id":r[0],"name":r[1],"primary":r[2],"secondary":r[3],"items":[]})
    w["items"].append({"n":r[4],"ex":r[5],"sets":"" if r[6] in (None,"") else str(r[6]),"reps":r[7]})
data = {
 "exercises":[dict(zip(["name","body","secondary","tags","sets","reps","equipment","notes","workout"],[("" if v is None else str(v)) for v in r])) for r in lib_r],
 "workouts":list(wk.values()),
 "coaching":{}
}
for m,sec,n,cue in cc_r:
    data["coaching"].setdefault(m,{}).setdefault(sec,[]).append(cue)
json.dump(data, open("data.json","w"), ensure_ascii=False)

html = open("app_template.html").read().replace("__FRIENDS__", "false").replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</","<\\/"))
open("gym-library.html","w").write(html)
