FROM python:3.8

WORKDIR /app

COPY . /app

# Update and install required packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends build-essential vim fonts-nanum

# Install Python dependencies
RUN pip install --no-cache-dir flask pandas numpy matplotlib seaborn scikit-learn

WORKDIR /usr/share/fonts/
RUN wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
RUN unzip NanumFont_TTF_ALL.zip -d NanumFont
RUN rm -f NanumFont_TTF_ALL.zip
RUN fc-cache -f -v

WORKDIR /app

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]