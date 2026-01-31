import { useState } from "react";
import {
  Button,
  Select,
  MenuItem,
  TextField,
  Checkbox,
  FormControlLabel,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Card,
  CardContent,
  Grid,
  ThemeProvider,
  createTheme,
  InputLabel,
  FormControl,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

/* ===== CAMPUS CONFIG (UI ONLY) ===== */
const INCIDENT_TYPES = [
  "Fire",
  "Harassment",
  "Medical",
  "Theft",
  "Lab Hazard",
  "Cyberbullying",
];

const LOCATIONS = [
  "Girls Hostel A","Girls Hostel B","Boys Hostel A","Boys Hostel B",
  "Yamuna Hostel","Ganga Hostel","KC Hostel",
  "Main Academic Block","Engineering Block","Management Block",
  "Computer Lab","AI Lab","Cyber Security Lab",
  "Central Library","Cafeteria",
  "Student Parking","Faculty Parking","GD Subway",
];

const USER_ROLES = ["Student","Faculty","Staff","Security"];

/* ===== THEME ===== */
const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#7c3aed" },
    background: {
      default: "#0b0715",
      paper: "#1a1033",
    },
  },
});

export default function App() {
  const [incidentType, setIncidentType] = useState("Fire");
  const [location, setLocation] = useState("Girls Hostel A");
  const [description, setDescription] = useState("");
  const [role, setRole] = useState("Student");
  const [panic, setPanic] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [step, setStep] = useState(0);

  const steps = [
    "Incident Intake",
    "Risk Evaluation",
    "Response Planning",
    "Audit & Governance",
  ];

  function handleSubmit() {
    if (!description.trim()) {
      alert("Please enter incident description");
      return;
    }

    setSubmitted(true);
    setStep(0);

    let i = 0;
    const interval = setInterval(() => {
      i++;
      setStep(i);
      if (i === steps.length) clearInterval(interval);
    }, 400);
  }

  return (
    <ThemeProvider theme={theme}>
      <div style={{ padding: 24 }}>

        {/* HERO */}
        <Card sx={{ mb: 3, p: 3, background: "linear-gradient(135deg,#6d28d9,#4c1d95)" }}>
          <h2>Autonomous Campus Safety Intelligence – GLA University</h2>
          <p>Config-Driven • Multi-Agent • Human-in-the-Loop</p>
        </Card>

        <Grid container spacing={3}>

          {/* INCIDENT INPUT */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <h3>📥 Incident Reporting</h3>

                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel>Incident Type</InputLabel>
                  <Select value={incidentType} label="Incident Type"
                    onChange={(e) => setIncidentType(e.target.value)}>
                    {INCIDENT_TYPES.map(t => (
                      <MenuItem key={t} value={t}>{t}</MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel>Location</InputLabel>
                  <Select value={location} label="Location"
                    onChange={(e) => setLocation(e.target.value)}>
                    {LOCATIONS.map(l => (
                      <MenuItem key={l} value={l}>{l}</MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  sx={{ mt: 2 }}
                  label="Description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />

                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel>User Role</InputLabel>
                  <Select value={role} label="User Role"
                    onChange={(e) => setRole(e.target.value)}>
                    {USER_ROLES.map(r => (
                      <MenuItem key={r} value={r}>{r}</MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <FormControlLabel
                  sx={{ mt: 1 }}
                  control={<Checkbox checked={panic}
                    onChange={(e) => setPanic(e.target.checked)} />}
                  label="🚨 Panic Mode"
                />

                <Button variant="contained" fullWidth sx={{ mt: 2 }}
                  onClick={handleSubmit}>
                  Submit Incident
                </Button>
              </CardContent>
            </Card>
          </Grid>

          {/* SNAPSHOT */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <h3>📊 Situation Snapshot</h3>
                {!submitted ? (
                  <p>System monitoring campus activity.</p>
                ) : (
                  <>
                    <p><b>Incident:</b> {incidentType}</p>
                    <p><b>Location:</b> {location}</p>
                    <p><b>Status:</b> {panic ? "Immediate Threat" : "Under Review"}</p>
                  </>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* AGENT PIPELINE */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <h3>🧠 AI Agent Pipeline</h3>
                <LinearProgress
                  variant="determinate"
                  value={(step / steps.length) * 100}
                  sx={{ my: 1 }}
                />
                {steps.map((s, i) => (
                  <div key={s}>{step > i ? "✔" : "○"} {s}</div>
                ))}
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* EXPLAINABILITY */}
        {submitted && (
          <Accordion sx={{ mt: 3 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              Why this decision?
            </AccordionSummary>
            <AccordionDetails>
              Decision derived from campus risk zones, incident type,
              operating hours, and institutional safety policies.
            </AccordionDetails>
          </Accordion>
        )}
      </div>
    </ThemeProvider>
  );
}
