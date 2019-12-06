import axios from 'axios';
// import { toast } from 'react-toastify';

let browserCurrentUrl = window.location.href;
let host = browserCurrentUrl.split("/")[2];
host = host.split(":")[0];

let apiUrl = `http://${host}:5000`
console.log(host, apiUrl)

export let url = apiUrl;

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

// usage examples
export const postStartMcts = (searchesPerMove, callback) => {
    let body = {
        searchesPerMove: searchesPerMove
    };

    post("/api/mcts/start", body, "Starting MCTS", callback);
}

// post example
export const getBenchmarkEnginesList = async () => {
    return await get("/api/benchmark/engines");
}

export default api;