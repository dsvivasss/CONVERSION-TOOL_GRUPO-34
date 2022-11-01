import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 1, // Virtual Users
    duration: '10s',
}

export function setup() {
    return oauth('daniel', 'nacional')
}


// Open a file to upload
const file = open(`/scripts/audios/audio25.wav`, 'b'); // 5MB file

export default function (token) {

    const data = {
        newFormat: 'mp3',
        fileName: http.file(file, 'audio25.wav'),
    };

    const test = http.post('http://34.136.168.9/api/tasks', data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    console.log(test)
}