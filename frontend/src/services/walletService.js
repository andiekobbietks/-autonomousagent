import API from './api';

export const getWallet = async () => {
  const response = await API.get('/wallets/me');
  return response.data;
};

export const getTransactions = async () => {
    const response = await API.get('/wallets/me/transactions');
    return response.data;
};

export const withdraw = async (withdrawalData) => {
    const response = await API.post('/wallets/me/withdraw', withdrawalData);
    return response.data;
};