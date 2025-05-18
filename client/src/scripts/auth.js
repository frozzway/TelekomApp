import AccountApi from "@/api/AccountApi.js";
import { jwtDecode } from "jwt-decode";

export const ACCESS_TOKEN_KEY = 'accessToken';

const accessTokenExpires = {
  get value() {
    const stored = localStorage.getItem(ACCESS_TOKEN_KEY);
    return stored ? jwtDecode(stored).exp : 0;
  }
};

const tokenTimeSkewSeconds = 30
let cachedRefreshTokenRequest = null
const now = () => Math.floor(Date.now() * 0.001)
const isAccessTokenValid = () => now() < accessTokenExpires.value - tokenTimeSkewSeconds;
const getAccessToken = () => localStorage.getItem(ACCESS_TOKEN_KEY);
export const setAccessToken = (token) => localStorage.setItem(ACCESS_TOKEN_KEY, token);
export const removeAccessToken = () => localStorage.removeItem(ACCESS_TOKEN_KEY);

async function refreshToken() {
  const { access_token } = await AccountApi.refreshToken()
  setAccessToken(access_token)
  return { accessToken: access_token }
}


export async function requestValidToken() {
  let accessToken = getAccessToken();
  if (!isAccessTokenValid()) {
    if (cachedRefreshTokenRequest === null) {
      cachedRefreshTokenRequest = refreshToken()
    }

    accessToken = (await cachedRefreshTokenRequest).accessToken;
    cachedRefreshTokenRequest = null;
  }

  return accessToken;
}