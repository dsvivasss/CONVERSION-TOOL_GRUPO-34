import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 10, // Virtual Users
    duration: '1m',
}

export function setup() {
    return '23'
}


// Open a file to upload
const file = open(`/scripts/audios/audio25.mp3`, 'b'); // 5MB file

export default function () {

    const data = {
        newFormat: 'ogg',
        fileName: http.file(file, 'audio25.mp3'),
    };

    const test = http.post('http://35.245.192.250:5001/api/tasks', data, {
        headers: {
            'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjkwOTgxMzQsImV4cCI6MTY2OTEwMTczNCwic3ViIjoiaXNtYWVsMiIsImlzcyI6Ind3dy50ZXN0LmNvbSJ9.0-PuJXVZT9pyvp08fq14qroIyRdLYH046Z_LU7NJ47s`
        }
    });
}