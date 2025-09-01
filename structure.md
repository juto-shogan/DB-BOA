/db-boa
├── README.md                   # Project overview & setup instructions
├── .gitignore                  # Ignore venv, logs, and artifacts if using Git
│
├── /database
│   ├── schema.sql              # SQL script for creating the e-commerce schema
│   ├── seed_data.sql           # SQL script to populate initial dummy data
│   ├── config.py               # DB connection settings (host, user, password, db)
│   └── setup.py                # Script to initialize database (schema + seed)
│
├── /simulation
│   ├── normal_traffic.py       # Simulates legitimate queries (users, admins)
│   ├── attack_bot.py           # Simulates malicious traffic (buffer overflow, SQLi)
│   ├── utils.py                # Helper functions (random data generation, logging)
│   ├── run_simulation.py       # Orchestrator for launching traffic + logging
│   └── logs/                   # Directory to store raw query logs
│
├── /model
│   ├── data_collection.py      # Extract logs and prepare training data
│   ├── feature_engineering.py  # Convert raw logs into ML-friendly features
│   ├── model_training.py       # Train anomaly detection model
│   ├── trained_model.pkl       # Saved trained model (binary file)
│   ├── evaluation.py           # Evaluate accuracy, precision, recall, F1
│   └── requirements.txt        # Python dependencies (scikit-learn, psycopg2, etc.)
│
├── /dashboard
│   ├── app.py                  # Flask/FastAPI backend for dashboard
│   ├── templates/              # HTML Jinja templates
│   │   ├── index.html          # Main dashboard
│   │   └── alerts.html         # Anomaly alert display
│   └── static/                 # CSS, JS, and assets
│       ├── style.css           # Styling
│       └── main.js             # Client-side logic
│
├── /docs
│   ├── proposal.docx           # Project proposal
│   ├── final_report.pdf        # Full project report
│   └── presentation_slides.pptx# Final presentation slides
│
└── /tests
    ├── test_database.py        # Unit tests for DB setup
    ├── test_simulation.py      # Unit tests for traffic simulation
    ├── test_model.py           # Unit tests for ML pipeline
    └── test_dashboard.py       # Unit tests for dashboard
