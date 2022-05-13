FROM node:13.12.0-alpine

# set working directory
WORKDIR /user/src/app

# install app dependencies
COPY ./package.json ./
RUN npm install --legacy-peer-deps

# add app
COPY . ./

EXPOSE 3000

# start app
CMD ["npm", "start"]