import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Wifi } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Fake login
    navigate('/dashboard');
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="flex justify-center mb-8">
        <div className="bg-primary/10 p-3 rounded-xl flex items-center gap-3">
          <Wifi className="h-8 w-8 text-primary" />
          <span className="text-3xl font-bold tracking-tight">WiSense</span>
        </div>
      </div>
      
      <Card className="border-border/50 shadow-lg">
        <CardHeader className="space-y-1 text-center pb-8">
          <CardTitle className="text-2xl font-bold">Welcome back</CardTitle>
          <CardDescription>
            Enter your email and password to access your account
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleLogin}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium leading-none" htmlFor="email">
                Email
              </label>
              <Input 
                id="email" 
                type="email" 
                placeholder="admin@wisense.io" 
                defaultValue="admin@wisense.io"
                required
              />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium leading-none" htmlFor="password">
                  Password
                </label>
                <a href="#" className="text-xs text-primary hover:underline">
                  Forgot password?
                </a>
              </div>
              <Input 
                id="password" 
                type="password"
                defaultValue="password123"
                required
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-4 pt-4">
            <Button type="submit" className="w-full">Sign In</Button>
            <p className="text-xs text-center text-muted-foreground">
              By clicking continue, you agree to our{' '}
              <a href="#" className="underline underline-offset-4 hover:text-primary">Terms of Service</a>{' '}
              and{' '}
              <a href="#" className="underline underline-offset-4 hover:text-primary">Privacy Policy</a>.
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
