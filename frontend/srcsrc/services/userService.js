import API from './api';

export const getUser = async () => {
  const response = await API.get('/users/me');
  return response.data;
};