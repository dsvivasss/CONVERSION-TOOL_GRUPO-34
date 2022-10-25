import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 10, // Virtual Users
    duration: '10s',
}

export function setup() {
    return oauth('miguel1', 'nacional')
}

// export const options = {
//   stages: [
//     { duration: '10s', target: 20 },
//   ],
// }

const files = [
    'audio.ogg', 'audio16.mp3', 'audio22.mp3', 'audio29.mp3', 'audio8.ogg',
    'audio10.ogg', 'audio17.mp3', 'audio23.wav', 'audio3.mp3', 'audio9.ogg',
    'audio11.mp3', 'audio18.mp3', 'audio24.wav', 'audio30.mp3',
    'audio12.mp3', 'audio19.mp3', 'audio25.wav', 'audio4.mp3',
    'audio13.mp3', 'audio2.mp3', 'audio26.wav', 'audio5.wav',
    'audio14.mp3', 'audio20.mp3', 'audio27.mp3', 'audio6.mp3',
    'audio15.mp3', 'audio21.mp3', 'audio28.mp3', 'audio7.ogg'
]

export default function (token) {

    // Get random value from files
    const randomFile = files[Math.floor(Math.random() * files.length)];
    // Open a file to upload
    const file = open(`./audios/${randomFile}`, 'b');

    const data = {
        newFormat: 'wma',
        fileName: http.file(file, randomFile),
    };

    http.post('http://host.docker.internal:5001/api/tasks', data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
}