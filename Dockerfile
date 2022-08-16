FROM node:alpine

ENV CHROME_BIN="/usr/bin/chromium-browser" \
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD="true" \
    LANDSCAPE_VERSION=latest \
    MMDC_CMD=/app/node_modules/.bin/mmdc

ARG VERSION

# Install chromium and required fonts
# available fonts https://wiki.alpinelinux.org/wiki/Fonts
RUN apk add chromium font-noto-cjk font-noto-emoji \
    terminus-font ttf-dejavu ttf-freefont ttf-font-awesome \
    ttf-inconsolata ttf-linux-libertine \
    && fc-cache -f

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN #adduser -D mermaidcli
#USER mermaidcli
#WORKDIR /home/mermaidcli
ADD . /app
ADD puppeteer-config.json  /puppeteer-config.json
WORKDIR /app

## Python script
RUN pip3 install -r /app/requirements.txt

RUN yarn add @mermaid-js/mermaid-cli@9.1.5

ENTRYPOINT ["python", "main.py"]
CMD [ "--help" ]
#
#ENTRYPOINT ["./node_modules/.bin/mmdc", "-p", "/puppeteer-config.json"]
#CMD [ "--help" ]