/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react';
import Button from '../components/Button';
import arch from '../images/architecture.gif';
import student from '../images/student.PNG';
import student_dash from '../images/student_dash.PNG';
import update from '../images/update.PNG';
import SCHub_title from '../images/SCHub-title.png';
import '../styles/home.css';

function Home() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const slides = [student, student_dash, update, arch];

  const changeSlide = (n) => {
    let newIndex = currentIndex + n;
    if (newIndex < 0) {
      newIndex = slides.length - 1;
    } else if (newIndex >= slides.length) {
      newIndex = 0;
    }
    setCurrentIndex(newIndex);
  };

  useEffect(() => {
    const interval = setInterval(() => {
      changeSlide(1);
    }, 15000);

    return () => {
      clearInterval(interval);
    };
  }, [currentIndex]);

  return (
    <div className='home'>
      <section id='intro'>
        <img src={SCHub_title} alt='SCHub Title' />
        <p className='intro'>
          SCHub is a web service for institutional data management and analysis.
          You can upload, store, query, and visualize your data using our web
          interface or API.
        </p>
        <div className='buttons'>
          <a href='https://www.schub.me/apidocs' className='button'>
            Documentation
          </a>
          <a href='https://github.com/micoliser/SCHub' className='button'>
            Repository
          </a>
          <a href='https://github.com/micoliser/SCHub' className='button'>
            Authors
          </a>
          <a
            href='https://www.linkedin.com/pulse/schub-project-jesulayomi-aina'
            className='button'
          >
            Blogpost
          </a>
          <a href='https://www.schub.me/explore/#about' className='button'>
            Profiles
          </a>
        </div>
      </section>
      <div id='features'>
        <h2>Features</h2>
        <ul>
          <li>Upload and store your data securely on our cloud server.</li>
          <li>Query your data using SQL or our custom query language.</li>
          <li>Visualize your data using charts, graphs, maps, and tables.</li>
          <li>Export your data or visualizations in various formats.</li>
          <li>
            Share your data or visualizations with others or embed them on your
            website.
          </li>
          <li>
            Access our RESTful API for more advanced features and integrations.
          </li>
        </ul>
      </div>
      <div id='slides' className='carousel'>
        <div className='carousel-inner'>
          {slides.map((slide, index) => (
            <img
              key={index}
              src={slide}
              alt={`Schub images`}
              className={index === currentIndex ? 'activate' : ''}
            />
          ))}
        </div>
        <Button className='carousel-prev' onClick={() => changeSlide(-1)}>
          &#10094;
        </Button>
        <Button className='carousel-next' onClick={() => changeSlide(1)}>
          &#10095;
        </Button>
      </div>
      <div id='announcements'>
        <h2>Announcements</h2>
        <div className='ann-border'>
          <div className='ann-left'>
            <p>
              We are excited to announce that SCHub is now live! You can start
              uploading, storing, querying, and visualizing your data today.
              Check out our blogpost for more details.
            </p>
            <p>
              We are also looking for contributors to join our team and help us
              improve SCHub. If you are interested, please visit our repository
              and follow the instructions.
            </p>
          </div>
          <div className='ann-right'>
            <div className='timeline'>
              <h3>Timeline</h3>
              <div className='time_row'>
                <div className='date'>
                  <p>18</p>
                </div>
                <div className='event'>
                  <p>Shutting down web server and loadbalancer, app server still active</p>
                </div>
              </div>
              <div className='time_row'>
                <div className='date'>
                  <p>15</p>
                </div>
                <div className='event'>
                  <p>Cleaning up the project files and pages</p>
                </div>
              </div>
              <div className='time_row'>
                <div className='date'>
                  <p>13</p>
                </div>
                <div className='event'>
                  <p>Dev complete!</p>
                </div>
              </div>
              <div className='time_row'>
                <div className='date'>
                  <p>&nbsp;7</p>
                </div>
                <div className='event'>
                  <p>First deployment</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div id='footer'>
        <p>
          &copy; 2023{' '}
          <a
            href='https://github.com/micoliser/SCHub/blob/main/LICENSE'
            alt='LICENSE'
          >
            SCHub.
          </a>{' '}
          All rights reserved.
        </p>
      </div>
    </div>
  );
}

export default Home;
