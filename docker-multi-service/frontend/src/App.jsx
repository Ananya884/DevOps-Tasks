import { useEffect, useState } from 'react';

export default function App() {
  const [health, setHealth] = useState('loading...');
  const [dbTime, setDbTime] = useState('loading...');

  useEffect(() => {
    fetch('/api/health')
      .then((r) => r.json())
      .then((d) => setHealth(d.status))
      .catch(() => setHealth('API unreachable'));

    fetch('/api/time')
      .then((r) => r.json())
      .then((d) => setDbTime(d.dbTime || d.error))
      .catch(() => setDbTime('API unreachable'));
  }, []);

  return (
    <div style={{ fontFamily: 'sans-serif', margin: '40px' }}>
      <h1>Multi-Service App</h1>
      <p>API health: <b>{health}</b></p>
      <p>Time from PostgreSQL: <b>{dbTime}</b></p>
    </div>
  );
}
