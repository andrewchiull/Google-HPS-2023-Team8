import React, { useEffect, useState } from "react";
import Image from "next/image";
import styles from "./homepage.module.scss";
import Link from "next/link";
import { useRouter } from "next/router";

const HomePage = () => {
  const [data, setData] = useState([]);
  const { createClient } = require("@supabase/supabase-js");
  const SERVICE_KEY = "your_supabase_service_key";

  const SUPABASE_URL = "your_supabase_url";

  const supabase = createClient(SUPABASE_URL, SERVICE_KEY);

  useEffect(() => {
    fetch("/api/getData")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);
  console.log(data);
  const bottomClothes = data.filter((item) => item.cloth_type === "bottom");
  const topClothes = data.filter((item) => item.cloth_type === "top");

  // 衣服
  console.log(topClothes);
  const [currentIndex, setCurrentIndex] = useState(0); // Track current index
  const handleNextClick = async () => {
    const nextIndex = (currentIndex + 1) % topClothes.length;
    await preloadImage(topClothes[nextIndex].photo_path);
    setCurrentIndex(nextIndex);
  };

  const handlePrevClick = async () => {
    const prevIndex =
      currentIndex === 0 ? topClothes.length - 1 : currentIndex - 1;
    await preloadImage(topClothes[prevIndex].photo_path);
    setCurrentIndex(prevIndex);
  };

  // 褲子
  const [currentIndexbottom, setCurrentIndexbottom] = useState(0); // Track current index
  const handleNextClickbottom = () => {
    setCurrentIndexbottom(
      (prevIndex) => (prevIndex + 1) % bottomClothes.length
    );
  };

  const handlePrevClickbottom = () => {
    setCurrentIndexbottom((prevIndex) =>
      prevIndex === 0 ? bottomClothes.length - 1 : prevIndex - 1
    );
  };

  const preloadImage = (url) => {
    return new Promise((resolve, reject) => {
      const img = new window.Image(); // Use the regular Image object
      img.src = url;
      img.onload = resolve;
      img.onerror = reject;
    });
  };

  const router = useRouter();

  const goToClothesPage = (id) => {
    router.push(`/clothes/${id}`);
    handleupdatedata(id);
  };

  const handleupdatedata = async (id) => {
    // 取得目前顯示的衣物資料

    // 更新資料庫中的資料
    try {
      const { data, error } = await supabase
        .from("closet")
        .update({ state: "OUT" }) // 假設有一個 worn_times 屬性用於記錄穿著次數
        .eq("id", id); // 根據 id 更新特定資料

      if (error) {
        console.error("Error updating data:", error);
      } else {
        console.log("Data updated successfully:", data);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return (
    <>
      <div className={styles.root}>
        <div className={styles.closet}>
          <div className={styles.smart}>
            <Image
              src="/Gootdle_logo_large.png"
              alt="gootdle"
              width={250}
              height={83}
              className={styles.gootdle}
            />
            <div className={styles.worddown}>SMART DRESSING ZERO MESSING</div>
          </div>
        </div>
        <div className={styles.line}></div>
        <div className={styles.season}>
          <div className={styles.word}>SPRING</div>
          <div className={styles.word}>SUMMER</div>
          <div className={styles.word}>AUTUMN</div>
          <div className={styles.word}>WINTER</div>
        </div>
        <div className={styles.line}></div>

        <div>
          <div>
            <div className={styles.top}>TOP</div>
            <div className={styles.all}>
              <Image
                src="/Polygon 4.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handlePrevClick}
                className={styles.tri}
              />

              {topClothes.length > 0 && currentIndex < topClothes.length ? (
                <div key={topClothes[currentIndex].id}>
                  <div
                    className={styles.cloth}
                    onClick={() => goToClothesPage(topClothes[currentIndex].id)}
                  >
                    <div className={styles.cloth}>
                      <img
                        src={topClothes[currentIndex].photo_path}
                        alt="TRI"
                        width={100}
                        height={97}
                      />
                      <div className={styles.info}>
                        {topClothes[currentIndex].color_name}
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className={styles.skeleton}></div>
              )}
              <Image
                src="/Polygon 1.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handleNextClick}
                className={styles.tri}
              />
            </div>
          </div>
          <div>
            <div className={styles.bottom}>BOTTOM</div>
            <div className={styles.all}>
              <Image
                src="/Polygon 4.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handlePrevClickbottom}
                className={styles.tri}
              />
              {bottomClothes.length > 0 &&
              currentIndexbottom < bottomClothes.length ? (
                <div key={bottomClothes[currentIndexbottom].id}>
                  <div
                    className={styles.cloth}
                    onClick={() =>
                      goToClothesPage(bottomClothes[currentIndexbottom].id)
                    }
                  >
                    <img
                      src={bottomClothes[currentIndexbottom].photo_path}
                      alt="TRI"
                      width={100}
                      height={97}
                    />
                    <div className={styles.info}>
                      {bottomClothes[currentIndexbottom].color_name}
                    </div>
                  </div>
                </div>
              ) : (
                <div className={styles.skeleton}></div>
              )}
              <Image
                src="/Polygon 1.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handleNextClickbottom}
                className={styles.tri}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default HomePage;
