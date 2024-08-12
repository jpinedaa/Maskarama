
import { type AppType } from "next/app";
import Layout from '~/components/shared/layout';
// import { ApiProvider } from '~/gameLogic/apiContext';
import { ApiProvider } from '~/gameLogic/apiContext';
import "~/styles/globals.css";

const AppInitializer: React.FC<{ children: React.ReactNode }> = ({ children }) => {

  return <>{children}</>;
};

const MyApp: AppType = ({ Component, pageProps }) => {

  

  return (
    <ApiProvider>
      <AppInitializer>
        <Layout >
          <Component {...pageProps} />
        </Layout>
      </AppInitializer>
    </ApiProvider>
  );
};

export default MyApp;