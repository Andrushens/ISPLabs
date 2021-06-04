FROM python:3.8.5-alpine

WORKDIR /usr/src/my_site

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev

RUN pip3 install --upgrade pip

COPY . .

COPY ./requirements.txt .
RUN pip3 install -U -r requirements.txt

RUN mkdir -p /home/project

RUN addgroup -S project && adduser -S project -G project

ENV HOME=/home/project
ENV APP_HOME=/home/project/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/static_dev
RUN mkdir $APP_HOME/mediafiles
RUN mkdir $APP_HOME/media_dev
WORKDIR $APP_HOME

COPY ./entrypoint.sh $APP_HOME

COPY . $APP_HOME

RUN chown -R project:project $APP_HOME

USER project

# ENTRYPOINT [ "/home/project/web/entrypoint.sh" ]