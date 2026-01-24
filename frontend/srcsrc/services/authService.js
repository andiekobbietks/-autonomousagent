import API, { setAuthToken } from './api';

export const register = async (userData) => {
  const response = await API.post('/users/register', userData);
  return response.data;
};

export const login = async (credentials) => {
  const response = await API.post('/users/login', credentials);
  if (response.data.access_token) {
    setAuthToken(response.data.access_token);
  }
  return response.data;
};

export const logout = () => {
  setAuthToken(null);
};