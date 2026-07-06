import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background text-center px-4">
      <h1 className="text-7xl font-bold tracking-tight text-primary">404</h1>
      <p className="mt-4 text-xl text-muted-foreground">
        The page you are looking for does not exist.
      </p>
      <div className="mt-8">
        <Button render={<Link to="/" />}>
          Go back home
        </Button>
      </div>
    </div>
  );
}
