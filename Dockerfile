COPY duplicator.py duplicator_runner.py manager_ui.py config.env ./
COPY templates/ ./templates/
CMD ["python3", "manager_ui.py"]
