import { ThreeDots } from 'react-loader-spinner';
import '../styles/loading.css';

function LoadingPage() {
  return (
    <div className='loading'>
      <div>
        <ThreeDots
          height='100'
          width='100'
          radius='12'
          color='#4fa94d'
          ariaLabel='three-dots-loading'
          wrapperStyle={{}}
          wrapperClassName=''
          visible={true}
        />
      </div>
      <h3>Loading page</h3>
    </div>
  );
}

export default LoadingPage;
