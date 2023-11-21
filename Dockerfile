FROM python:3.8

WORKDIR /app

COPY . /app

# Update and install required packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends build-essential 

# Install Python dependencies
RUN pip install --no-cache-dir flask pandas numpy matplotlib seaborn scikit-learn

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]