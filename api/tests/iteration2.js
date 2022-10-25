import http from 'k6/http';
import { oauth } from './oauth.js';

export const options = {
  vus: 10, // Virtual Users
  duration: '10s',
}

export function setup () {
    return oauth('miguel1', 'nacional')
}

// export const options = {
//   stages: [
//     { duration: '10s', target: 20 },
//   ],
// }

// Open a file to upload
const file = open('./audio.ogg', 'b');

export default function (token) {

  const data = {
    newFormat: 'ogg',
    fileName: http.file(file, 'audio2.mp3'),
  };

  http.post('http://host.docker.internal:5001/api/tasks', data, {
    headers: {
        'Authorization': `Bearer ${token}`
    }
  });
}