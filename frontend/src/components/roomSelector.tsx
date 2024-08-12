// roomSelector.tsx
import React from 'react';
import { useAtom } from 'jotai';
import { environmentsAtom, currentEnvironmentAtom } from '~/gameLogic/gameStateManager';
import { useApi } from '~/gameLogic/apiContext';

const RoomSelector: React.FC = () => {
  const [environments] = useAtom(environmentsAtom);
  const [currentEnvironment, setCurrentEnvironment] = useAtom(currentEnvironmentAtom);
  const apiService = useApi();

  const handleRoomChange = async (newRoomId: string) => {
    if (newRoomId !== currentEnvironment) {
      await apiService.startSimulation(1); // Simulate moving to a new room
      setCurrentEnvironment(newRoomId);
    }
  };

  return (
    <div>
      <h3>Select Room:</h3>
      {Object.keys(environments).map(roomId => (
        <button
          key={roomId}
          onClick={() => handleRoomChange(roomId)}
          disabled={roomId === currentEnvironment}
        >
          {roomId}
        </button>
      ))}
    </div>
  );
};

export default RoomSelector;