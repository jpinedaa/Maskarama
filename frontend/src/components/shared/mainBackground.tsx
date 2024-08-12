import Image from 'next/image';

const MainBackground: React.FC = () => {
  return (
    <div className='absolute inset-auto h-full w-full'>
          <div className="relative w-full h-full">
            <Image 
              src={'/webp/mainbackground.webp'} 
              fill
              alt='bg'
            />
          </div>
        </div>
  )
}

export default MainBackground;