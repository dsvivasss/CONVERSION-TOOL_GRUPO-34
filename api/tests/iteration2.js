import http from 'k6/http';

export const options = {
  vus: 10, // Virtual Users
  duration: '10s',
}

export function setup () {
    const urlToken = 'http://host.docker.internal:5001/api/auth/login'

    const data = {
        username: 'miguel1',
        password: 'nacional'
    }

    const response = http.post(urlToken, JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return response.json('token')
}

// export const options = {
//   stages: [
//     { duration: '10s', target: 20 },
//   ],
// }

// Open a file to upload
const file = open('./audio.ogg', 'b');

export default function (token) {

    console.log({token})

  const data = {
    newFormat: 'mp3',
    fileName: http.file(file, 'postgresImagen'),
  };

  http.post('http://host.docker.internal:5001/api/tasks/', data, {
    headers: {
        // 'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
    }
  });
}

import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";
import { textSummary } from "https://jslib.k6.io/k6-summary/0.0.1/index.js";

export function handleSummary(data) {
  return {
    "result.html": htmlReport(data),
    stdout: textSummary(data, { indent: " ", enableColors: true }),
  };
}