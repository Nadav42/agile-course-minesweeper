import axios from 'axios';
import { toast } from 'react-toastify';

let browserCurrentUrl = window.location.href;
let host = browserCurrentUrl.split("/")[2];
host = host.split(":")[0];

let apiUrl = `http://${host}:5000`
console.log(host, apiUrl)

export let url = apiUrl;
export let socket_host = `${host}:5000`;

// axios
let api = axios.create({
    baseURL: url
});

// GET REQUEST Helper
const get = async (endpointUrl, params) => {

    if (!params) {
        params = {};
    }

    try {
        const response = await api.get(`${url}${endpointUrl}`, { withCredentials: true, params: params });
        return response.data;
    }
    catch (error) {
        console.log(error);
    }

    return null;
}

// POST REQUEST Helper
const post = async (endpointUrl, bodyData, callback) => {
    api.post(`${url}${endpointUrl}`, bodyData, { withCredentials: true })
        .then((response) => {
            if (response.data["errorMsg"]) {
                toast.error(response.data["errorMsg"])
            }

            if (callback) {
                callback();
            }
        }, (error) => {
            console.log(error);
        });
}

// ---------- api ---------- //

// get board
export const getMinesweeperBoard = async () => {
    return await get("/api/board/fetch");
}

// get difficulty options (min-max range)
export const getDifficultyRange = async () => {
    return await get("/api/board/difficultyrange");
}

// board normal click
export const postBoardClick = (row, col, callback) => {
    let body = {
        row: row,
        col: col
    };

    post("/api/board/click", body, callback);
}

// board flag click
export const postBoardFlagClick = (row, col, callback) => {
    let body = {
        row: row,
        col: col
    };

    post("/api/board/flag", body, callback);
}

// board reset
export const postBoardReset = (rows, cols, difficulty, callback) => {
    let body = {
        rows: rows,
        cols: cols,
        difficulty: difficulty
    };

    post("/api/board/reset", body, callback);
}

// post example
export const getBenchmarkEnginesList = async () => {
    return await get("/api/benchmark/engines");
}

export default api;