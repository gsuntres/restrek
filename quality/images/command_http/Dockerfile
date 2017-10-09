FROM alpine:3.6
LABEL authors="George Suntres <gsuntres@gmail.coim>"
RUN apk --update add nodejs nodejs-npm bash git
COPY package.json /www/package.json
RUN cd /www; npm install
COPY . /www
WORKDIR /www
ENV PORT 4501
EXPOSE  4501:4501
CMD ["npm", "start"]
