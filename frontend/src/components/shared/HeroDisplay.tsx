import { useAtom } from 'jotai';
import { currentCharsInRoomAtom, gameStartedAtom, currentCharacterAtom } from '~/gameLogic/gameStateManager';

const HeroDisplay: React.FC = () => {
    const [currentCharsInRoom] = useAtom(currentCharsInRoomAtom);
    const [currentChar] = useAtom(currentCharacterAtom);
    const [gameStarted] = useAtom(gameStartedAtom);
    
    return (
        <div className={`absolute top-[81.5vh] md:top-[78vh]  left-0 z-20 w-full bg-transparent md:flex-row justify-center md:flex-wrap md:gap-2 ${gameStarted ? 'flex' : 'hidden'}`}>
            {currentCharsInRoom.map((hero, index) => (
                <div 
                    key={index} 
                    className={`relative w-[70px] h-[70px] sm:w-[100px] sm:h-[100px] shadow-lg}`}
                >
                    <div className='relative w-full h-3/4 z-10 bg-transparent border-2 border-parchment overflow-hidden'>
                        <video
                            autoPlay
                            loop
                            muted
                            playsInline
                            className='object-cover object-[95%_20%] w-full h-full'
                        >
                            <source src={hero.portrait} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    <h4 className={`relative  z-20 font-semibold text-sm sm:text-xl bg-white w-full text-center`}>{hero.name}</h4>
                </div>
            ))}
        </div>
    );
}

export default HeroDisplay;