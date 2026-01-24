import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../components/Input';
import Button from '../components/Button';
import { login } from '../services/authService';

const LoginScreen = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(formData);
            navigate('/dashboard');
        } catch (error) {
            console.error('Login failed', error);
        }
    };

    return (
        <div className="bg-background-dark text-white min-h-screen flex flex-col items-center justify-center">
            <div className="w-full max-w-md p-8 space-y-8">
                <h1 className="text-white tracking-tight text-[36px] font-bold leading-tight text-center">Login</h1>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="flex flex-col">
                        <label className="text-white/80 text-sm font-medium leading-normal pb-2 ml-1">Username</label>
                        <Input name="username" placeholder="Enter your username" type="text" onChange={handleChange} />
                    </div>
                    <div className="flex flex-col">
                        <label className="text-white/80 text-sm font-medium leading-normal pb-2 ml-1">Password</label>
                        <Input name="password" placeholder="Enter your password" type="password" onChange={handleChange} />
                    </div>
                    <Button type="submit" className="w-full bg-primary text-white text-lg">
                        Login
                    </Button>
                </form>
            </div>
        </div>
    );
};

export default LoginScreen;