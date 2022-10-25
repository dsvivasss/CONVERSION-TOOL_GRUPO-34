import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 50, // Virtual Users
    duration: '1m',
}

export function setup() {
    return oauth('miguel1', 'nacional')
}


// Open a file to upload
const file = open(`/scripts/audios/audio5.wav`, 'b'); // 5MB file

export default function (token) {

    const data = {
        newFormat: 'mp3',
        fileName: http.file(file, 'audio5.wav'),
    };

    http.post('http://host.docker.internal:5001/api/tasks', data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
}