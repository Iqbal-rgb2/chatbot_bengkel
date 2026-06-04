BEGIN TRANSACTION;
CREATE TABLE "barang" (
	"id_barang"	INTEGER,
	"nama_barang"	TEXT NOT NULL,
	"kategori"	TEXT NOT NULL,
	"stok"	INTEGER NOT NULL,
	"harga"	INTEGER NOT NULL,
	"cocok_untuk"	TEXT NOT NULL,
	PRIMARY KEY("id_barang" AUTOINCREMENT)
);
INSERT INTO "barang" VALUES(1,'Oli Yamalube Matic','oli',15,65000,'mio, fino, beat, vario, scoopy');
INSERT INTO "barang" VALUES(2,'Oli AHM MPX 2','oli',12,70000,'beat, vario, scoopy, pcx');
INSERT INTO "barang" VALUES(3,'Oli Enduro Matic','oli',10,68000,'mio, nmax, aerox');
INSERT INTO "barang" VALUES(4,'Busi NGK CPR9EA','busi',20,25000,'beat, vario, scoopy');
INSERT INTO "barang" VALUES(5,'Busi Denso U22EPR9','busi',18,28000,'mio, fino, lexi');
INSERT INTO "barang" VALUES(6,'Aki GS Astra GTZ5S','aki',8,260000,'beat, scoopy, vario');
INSERT INTO "barang" VALUES(7,'Aki Yuasa YTZ5S','aki',6,280000,'beat, vario, pcx');
INSERT INTO "barang" VALUES(8,'Ban FDR Sport XR Evo','ban',10,250000,'beat, vario, scoopy');
INSERT INTO "barang" VALUES(9,'Ban IRC NR76','ban',9,230000,'mio, fino, beat');
INSERT INTO "barang" VALUES(10,'Kampas Rem Federal','kampas rem',25,45000,'beat, vario, scoopy');
INSERT INTO "barang" VALUES(11,'Kampas Rem Indoparts','kampas rem',20,40000,'mio, fino');
INSERT INTO "barang" VALUES(12,'Filter Udara Honda','filter udara',10,35000,'beat, vario, scoopy');
INSERT INTO "barang" VALUES(13,'Filter Udara Yamaha','filter udara',8,38000,'mio, fino, nmax');
INSERT INTO "barang" VALUES(14,'CVT Belt Bando','cvt',7,120000,'beat, vario, scoopy');
INSERT INTO "barang" VALUES(15,'Rantai SSS','rantai',12,150000,'supra, jupiter, vega');
INSERT INTO "barang" VALUES(16,'Knalpot Racing Proliner','knalpot',6,450000,'');
INSERT INTO "barang" VALUES(17,'Knalpot Standar','knalpot',5,250000,'');
INSERT INTO "barang" VALUES(18,'Spion Mio','spion',12,32000,'');
INSERT INTO "barang" VALUES(19,'Spion Vario 125','spion',8,35000,'');
INSERT INTO "barang" VALUES(20,'Filter Oli AHM','filter oli',15,28000,'');
INSERT INTO "barang" VALUES(21,'Filter Oli Yamalube','filter oli',10,30000,'');
INSERT INTO "barang" VALUES(22,'Kampas Kopling Matic','kampas kopling',7,90000,'');
INSERT INTO "barang" VALUES(23,'Kampas Kopling Bebek','kampas kopling',6,85000,'');
INSERT INTO "barang" VALUES(24,'Roller CVT 15x12','roller',14,45000,'');
INSERT INTO "barang" VALUES(25,'Roller CVT 16x13','roller',10,47000,'');
INSERT INTO "barang" VALUES(26,'CDI Yamaha Mio','cdi',5,150000,'');
INSERT INTO "barang" VALUES(27,'CDI Honda Beat','cdi',4,155000,'');
INSERT INTO "barang" VALUES(28,'Kabel Busi','sparepart',20,20000,'');
INSERT INTO "barang" VALUES(29,'Kabel Kopling','sparepart',18,25000,'');
INSERT INTO "barang" VALUES(30,'Karet Gas','sparepart',15,17000,'');
INSERT INTO "barang" VALUES(31,'Switch Starter','switch',10,40000,'');
INSERT INTO "barang" VALUES(32,'Relay Starter','switch',5,50000,'');
INSERT INTO "barang" VALUES(33,'Karburator Yamaha','karburator',2,325000,'');
INSERT INTO "barang" VALUES(34,'Karburator Honda','karburator',3,340000,'');
INSERT INTO "barang" VALUES(35,'Rantai SSS 428','rantai',9,155000,'');
INSERT INTO "barang" VALUES(36,'Velg Depan','velg',2,400000,'');
INSERT INTO "barang" VALUES(37,'Velg Belakang','velg',2,450000,'');
INSERT INTO "barang" VALUES(38,'Lampu Depan LED','lampu',10,120000,'');
INSERT INTO "barang" VALUES(39,'Lampu Sen LED','lampu',10,45000,'');
INSERT INTO "barang" VALUES(40,'Kampas Rem Cakram','rem cakram',12,65000,'');
INSERT INTO "barang" VALUES(41,'Cakram Depan','rem cakram',4,120000,'');
INSERT INTO "barang" VALUES(42,'Master Rem Depan','rem cakram',3,175000,'');
INSERT INTO "barang" VALUES(43,'Shockbreaker Depan','sparepart',6,250000,'');
INSERT INTO "barang" VALUES(44,'Shockbreaker Belakang','sparepart',5,270000,'');
INSERT INTO "barang" VALUES(45,'Busi NGK KR7A','busi',15,26000,'');
INSERT INTO "barang" VALUES(46,'Aki Yuasa YTX7A-BS','aki',5,300000,'');
CREATE TABLE "chatbot_data" (
	"id_chatbot"	INTEGER,
	"intent"	TEXT NOT NULL,
	"pertanyaan"	TEXT NOT NULL,
	"jawaban"	TEXT NOT NULL,
	"action"	TEXT,
	PRIMARY KEY("id_chatbot" AUTOINCREMENT)
);
INSERT INTO "chatbot_data" VALUES(1,'sapaan','halo','Halo! Ada yang bisa saya bantu terkait layanan Bengkel Motor Kurnia?','');
INSERT INTO "chatbot_data" VALUES(2,'sapaan','hai','Halo! Ada yang bisa saya bantu terkait layanan Bengkel Motor Kurnia?','');
INSERT INTO "chatbot_data" VALUES(3,'sapaan','hallo','Halo! Ada yang bisa saya bantu terkait layanan Bengkel Motor Kurnia?','');
INSERT INTO "chatbot_data" VALUES(4,'sapaan','selamat pagi','Selamat pagi, ada yang bisa kami bantu?','');
INSERT INTO "chatbot_data" VALUES(5,'sapaan','selamat siang','Selamat siang, silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(6,'sapaan','selamat sore','Selamat sore, ada yang bisa dibantu?','');
INSERT INTO "chatbot_data" VALUES(7,'sapaan','permisi','Halo, silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(8,'sapaan','assalamualaikum','Waalaikumsalam, ada yang bisa dibantu?','');
INSERT INTO "chatbot_data" VALUES(9,'sapaan','salam','Halo, selamat datang di Bengkel Motor Kurnia.','');
INSERT INTO "chatbot_data" VALUES(10,'sapaan','pagi bengkel','Selamat pagi, ada yang bisa dibantu?','');
INSERT INTO "chatbot_data" VALUES(11,'sapaan','halo bengkel','Halo! Ada yang bisa saya bantu terkait layanan bengkel?','');
INSERT INTO "chatbot_data" VALUES(12,'sapaan','hai admin','Halo! Silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(13,'sapaan','selamat malam','Halo, pesan Anda tetap dapat ditanyakan melalui chatbot ini.','');
INSERT INTO "chatbot_data" VALUES(14,'sapaan','punten bengkel','Halo, silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(15,'bantuan_umum','tolong bantu saya','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(16,'bantuan_umum','bantu saya','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(17,'bantuan_umum','bisa bantu saya','Tentu, silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(18,'bantuan_umum','saya butuh bantuan','Silakan tanyakan layanan bengkel yang Anda butuhkan.','');
INSERT INTO "chatbot_data" VALUES(19,'bantuan_umum','bantu dong','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(20,'bantuan_umum','chatbot ini bisa apa','Saya dapat membantu lokasi bengkel, jadwal, servis motor, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(21,'bantuan_umum','fitur chatbot apa saja','Saya dapat membantu lokasi bengkel, jadwal, servis motor, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(22,'bantuan_umum','kamu bisa bantu apa','Saya dapat membantu informasi bengkel, stok barang, dan keluhan motor sederhana.','');
INSERT INTO "chatbot_data" VALUES(23,'bantuan_umum','saya mau tanya','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(24,'bantuan_umum','mau tanya dong','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(25,'bantuan_umum','butuh informasi bengkel','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(26,'bantuan_umum','help','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(27,'bantuan_umum','ada yang bisa dibantu','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(28,'bantuan_umum','informasi apa saja yang tersedia','Saya dapat membantu lokasi bengkel, jadwal, servis motor, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(29,'akhir_percakapan','terima kasih','Sama-sama, semoga membantu.','');
INSERT INTO "chatbot_data" VALUES(30,'akhir_percakapan','makasih','Sama-sama, hati-hati di jalan.','');
INSERT INTO "chatbot_data" VALUES(31,'akhir_percakapan','matur nuwun','Sama-sama, semoga membantu.','');
INSERT INTO "chatbot_data" VALUES(32,'akhir_percakapan','sudah cukup','Baik, terima kasih telah menggunakan layanan chatbot bengkel.','');
INSERT INTO "chatbot_data" VALUES(33,'akhir_percakapan','cukup','Baik, semoga informasi yang diberikan membantu.','');
INSERT INTO "chatbot_data" VALUES(34,'akhir_percakapan','itu saja','Baik, terima kasih sudah menghubungi bengkel kami.','');
INSERT INTO "chatbot_data" VALUES(35,'akhir_percakapan','tidak ada pertanyaan lagi','Baik, terima kasih sudah menghubungi bengkel kami.','');
INSERT INTO "chatbot_data" VALUES(36,'akhir_percakapan','sudah jelas','Baik, terima kasih telah menggunakan layanan chatbot bengkel.','');
INSERT INTO "chatbot_data" VALUES(37,'akhir_percakapan','oke makasih','Sama-sama, semoga harimu menyenangkan.','');
INSERT INTO "chatbot_data" VALUES(38,'akhir_percakapan','bye','Terima kasih telah menggunakan layanan chatbot bengkel.','');
INSERT INTO "chatbot_data" VALUES(39,'akhir_percakapan','sampai jumpa','Sampai jumpa kembali.','');
INSERT INTO "chatbot_data" VALUES(40,'akhir_percakapan','ok sip','Baik, semoga informasi yang diberikan membantu.','');
INSERT INTO "chatbot_data" VALUES(41,'jadwal_bengkel','bengkel buka jam berapa','Bengkel buka pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(42,'jadwal_bengkel','jam operasional bengkel','Bengkel buka Senin-Sabtu pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(43,'jadwal_bengkel','hari ini buka tidak','Bengkel buka Senin-Sabtu pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(44,'jadwal_bengkel','buka sampai jam berapa','Bengkel melayani sampai pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(45,'jadwal_bengkel','bengkel tutup jam berapa','Bengkel tutup pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(46,'jadwal_bengkel','hari minggu buka tidak','Bengkel libur pada hari Minggu.','');
INSERT INTO "chatbot_data" VALUES(47,'jadwal_bengkel','sabtu buka tidak','Bengkel buka hari Senin-Sabtu.','');
INSERT INTO "chatbot_data" VALUES(48,'jadwal_bengkel','bisa servis sore','Bengkel melayani servis sampai pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(49,'jadwal_bengkel','jadwal bengkel gimana','Bengkel buka Senin-Sabtu pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(50,'jadwal_bengkel','buka dari pagi jam berapa','Bengkel buka mulai pukul 08.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(51,'jadwal_bengkel','bengkel libur hari apa','Bengkel libur hari Minggu.','');
INSERT INTO "chatbot_data" VALUES(52,'jadwal_bengkel','masih buka sekarang','Bengkel buka sampai pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(53,'lokasi_bengkel','alamat bengkel dimana','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(54,'lokasi_bengkel','lokasi bengkel dimana','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(55,'lokasi_bengkel','bengkel ada dimana','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(56,'lokasi_bengkel','share lokasi bengkel','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(57,'lokasi_bengkel','ada maps bengkel','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(58,'lokasi_bengkel','kirim alamat bengkel','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(59,'lokasi_bengkel','bengkel dekat mana','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(60,'lokasi_bengkel','rute ke bengkel gimana','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(61,'lokasi_bengkel','posisi bengkel dimana','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(62,'lokasi_bengkel','lokasi lengkap bengkel','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(63,'lokasi_bengkel','maps kurnia motor','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(64,'lokasi_bengkel','saya mau ke bengkel','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(65,'kontak_admin','nomor wa bengkel berapa','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(66,'kontak_admin','wa bengkel berapa','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(67,'kontak_admin','nomor whatsapp bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(68,'kontak_admin','bisa hubungi lewat whatsapp','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(69,'kontak_admin','kontak admin ada','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(70,'kontak_admin','nomor telepon bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(71,'kontak_admin','minta nomor admin','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(72,'kontak_admin','saya mau chat petugas','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(73,'kontak_admin','hubungi petugas bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(74,'kontak_admin','nomor bengkel berapa','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(75,'kontak_admin','kontak bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(76,'kontak_admin','admin bisa dihubungi','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(77,'harga_servis','ganti oli motor berapa','Biaya ganti oli mulai Rp50.000, belum termasuk harga oli tertentu.','');
INSERT INTO "chatbot_data" VALUES(78,'harga_servis','servis motor berapa','Biaya servis motor mulai dari Rp75.000.','');
INSERT INTO "chatbot_data" VALUES(79,'harga_servis','servis lengkap habis berapa','Biaya servis lengkap mulai dari Rp150.000.','');
INSERT INTO "chatbot_data" VALUES(80,'harga_servis','tune up motor berapa','Biaya tune up mulai dari Rp100.000.','');
INSERT INTO "chatbot_data" VALUES(81,'harga_servis','servis ringan berapa','Biaya servis ringan mulai dari Rp75.000.','');
INSERT INTO "chatbot_data" VALUES(82,'harga_servis','cek motor bayar tidak','Pengecekan motor gratis.','');
INSERT INTO "chatbot_data" VALUES(83,'harga_servis','biaya cek kerusakan motor','Pengecekan motor gratis.','');
INSERT INTO "chatbot_data" VALUES(84,'harga_servis','tarif servis matic','Biaya servis motor matic mulai dari Rp75.000.','');
INSERT INTO "chatbot_data" VALUES(85,'harga_servis','harga servis injeksi','Biaya servis injeksi menyesuaikan kondisi motor.','');
INSERT INTO "chatbot_data" VALUES(86,'harga_servis','berapa biaya perbaikan rem','Biaya perbaikan rem menyesuaikan kondisi dan sparepart.','');
INSERT INTO "chatbot_data" VALUES(87,'harga_servis','biaya ganti ban','Biaya penggantian ban menyesuaikan jenis ban.','');
INSERT INTO "chatbot_data" VALUES(88,'harga_servis','harga tune up bengkel','Biaya tune up mulai dari Rp100.000.','');
INSERT INTO "chatbot_data" VALUES(89,'layanan_servis','motor saya brebet','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(90,'layanan_servis','motor brebet saat digas','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(91,'layanan_servis','motor brebet di tanjakan','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(92,'layanan_servis','motor brebet saat dingin','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(93,'layanan_servis','motor susah hidup','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(94,'layanan_servis','rem motor keras','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(95,'layanan_servis','mesin motor cepat panas','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(96,'layanan_servis','bisa servis motor matic','Bengkel melayani servis motor matic.','');
INSERT INTO "chatbot_data" VALUES(97,'layanan_servis','bisa servis injeksi','Bengkel menerima servis injeksi.','');
INSERT INTO "chatbot_data" VALUES(98,'layanan_servis','bisa tune up motor','Bengkel melayani tune up motor.','');
INSERT INTO "chatbot_data" VALUES(99,'layanan_servis','bisa ganti ban','Bengkel melayani penggantian ban.','');
INSERT INTO "chatbot_data" VALUES(100,'layanan_servis','bisa ganti oli','Bengkel melayani penggantian oli.','');
INSERT INTO "chatbot_data" VALUES(101,'layanan_servis','bisa perbaiki rem motor','Bengkel melayani perbaikan rem motor.','');
INSERT INTO "chatbot_data" VALUES(102,'layanan_servis','servis motor karburator bisa','Bengkel melayani servis motor karburator.','');
INSERT INTO "chatbot_data" VALUES(103,'layanan_servis','servis motor beat bisa','Bengkel melayani servis motor Beat.','');
INSERT INTO "chatbot_data" VALUES(104,'layanan_servis','servis motor vario bisa','Bengkel melayani servis motor Vario.','');
INSERT INTO "chatbot_data" VALUES(105,'cek_stok','stok oli yamalube matic','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(106,'cek_stok','ada oli ahm mpx 2','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(107,'cek_stok','oli enduro matic ready','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(108,'cek_stok','stok busi ngk cpr9ea','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(109,'cek_stok','ada busi denso u22epr9','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(110,'cek_stok','stok aki gs astra','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(111,'cek_stok','aki yuasa masih ada','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(112,'cek_stok','ban fdr ready','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(113,'cek_stok','ban irc masih tersedia','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(114,'cek_stok','kampas rem federal ada','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(115,'cek_stok','kampas rem indoparts ready','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(116,'cek_stok','filter udara honda ada','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(117,'cek_stok','filter udara yamaha tersedia','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(118,'cek_stok','cvt belt bando ada','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(119,'cek_stok','rantai sss ready','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(120,'cek_stok','stok oli untuk beat','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(121,'cek_stok','stok busi untuk vario','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(122,'cek_stok','stok aki untuk scoopy','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(123,'info_barang','informasi oli yamalube matic','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(124,'info_barang','harga oli ahm mpx 2','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(125,'info_barang','detail oli enduro matic','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(126,'info_barang','info busi ngk cpr9ea','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(127,'info_barang','harga busi denso u22epr9','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(128,'info_barang','informasi aki gs astra','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(129,'info_barang','detail aki yuasa','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(130,'info_barang','harga ban fdr sport','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(131,'info_barang','info ban irc nr76','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(132,'info_barang','harga kampas rem federal','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(133,'info_barang','detail kampas rem indoparts','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(134,'info_barang','info filter udara honda','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(135,'info_barang','harga filter udara yamaha','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(136,'info_barang','detail cvt belt bando','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(137,'info_barang','harga rantai sss','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(138,'info_barang','harga oli untuk beat','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(139,'info_barang','info aki untuk vario','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(140,'info_barang','detail sparepart motor','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(141,'rekom_produk','oli yang cocok untuk beat','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(142,'rekom_produk','rekomendasi oli vario','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(143,'rekom_produk','oli bagus untuk scoopy','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(144,'rekom_produk','oli untuk motor matic','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(145,'rekom_produk','busi yang cocok untuk beat','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(146,'rekom_produk','busi untuk vario apa','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(147,'rekom_produk','aki terbaik untuk nmax','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(148,'rekom_produk','aki untuk pcx apa','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(149,'rekom_produk','ban yang cocok untuk beat','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(150,'rekom_produk','produk cocok untuk mio','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(151,'daftar_barang','oli yang tersedia ada apa saja','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(152,'daftar_barang','oli apa saja yang ada','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(153,'daftar_barang','daftar oli yang tersedia','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(154,'daftar_barang','pilihan oli di bengkel apa saja','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(155,'daftar_barang','busi yang tersedia ada apa saja','Berikut daftar busi yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(156,'daftar_barang','daftar aki yang ada','Berikut daftar aki yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(157,'daftar_barang','ban apa saja yang tersedia','Berikut daftar ban yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(158,'daftar_barang','sparepart yang tersedia apa saja','Berikut daftar sparepart yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(159,'daftar_barang','barang yang tersedia di bengkel apa saja','Berikut daftar barang yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(160,'daftar_barang','ada pilihan filter udara apa saja','Berikut daftar filter udara yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(161,'sapaan','halo min','Halo! Ada yang bisa saya bantu terkait layanan Bengkel Motor Kurnia?','');
INSERT INTO "chatbot_data" VALUES(162,'sapaan','hai min','Halo! Ada yang bisa saya bantu terkait layanan Bengkel Motor Kurnia?','');
INSERT INTO "chatbot_data" VALUES(163,'sapaan','hallo min','Halo! Ada yang bisa saya bantu terkait layanan Bengkel Motor Kurnia?','');
INSERT INTO "chatbot_data" VALUES(164,'sapaan','selamat pagi min','Selamat pagi, ada yang bisa kami bantu?','');
INSERT INTO "chatbot_data" VALUES(165,'sapaan','selamat siang min','Selamat siang, silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(166,'sapaan','selamat sore min','Selamat sore, ada yang bisa dibantu?','');
INSERT INTO "chatbot_data" VALUES(167,'sapaan','permisi min','Halo, silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(168,'sapaan','assalamualaikum min','Waalaikumsalam, ada yang bisa dibantu?','');
INSERT INTO "chatbot_data" VALUES(169,'sapaan','salam min','Halo, selamat datang di Bengkel Motor Kurnia.','');
INSERT INTO "chatbot_data" VALUES(170,'sapaan','pagi bengkel min','Selamat pagi, ada yang bisa dibantu?','');
INSERT INTO "chatbot_data" VALUES(171,'sapaan','halo bengkel min','Halo! Ada yang bisa saya bantu terkait layanan bengkel?','');
INSERT INTO "chatbot_data" VALUES(172,'sapaan','hai admin min','Halo! Silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(173,'sapaan','selamat malam min','Halo, pesan Anda tetap dapat ditanyakan melalui chatbot ini.','');
INSERT INTO "chatbot_data" VALUES(174,'sapaan','punten bengkel min','Halo, silakan tanyakan kebutuhan Anda.','');
INSERT INTO "chatbot_data" VALUES(175,'bantuan_umum','min, tolong bantu saya','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(176,'bantuan_umum','min, bantu saya','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(177,'bantuan_umum','min, bisa bantu saya','Tentu, silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(178,'bantuan_umum','min, saya butuh bantuan','Silakan tanyakan layanan bengkel yang Anda butuhkan.','');
INSERT INTO "chatbot_data" VALUES(179,'bantuan_umum','min, bantu dong','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(180,'bantuan_umum','min, chatbot ini bisa apa','Saya dapat membantu lokasi bengkel, jadwal, servis motor, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(181,'bantuan_umum','min, fitur chatbot apa saja','Saya dapat membantu lokasi bengkel, jadwal, servis motor, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(182,'bantuan_umum','min, kamu bisa bantu apa','Saya dapat membantu informasi bengkel, stok barang, dan keluhan motor sederhana.','');
INSERT INTO "chatbot_data" VALUES(183,'bantuan_umum','min, saya mau tanya','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(184,'bantuan_umum','min, mau tanya dong','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(185,'bantuan_umum','min, butuh informasi bengkel','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(186,'bantuan_umum','min, help','Silakan tanyakan kebutuhan Anda terkait bengkel motor.','');
INSERT INTO "chatbot_data" VALUES(187,'bantuan_umum','min, ada yang bisa dibantu','Saya dapat membantu informasi bengkel, jadwal, lokasi, servis, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(188,'bantuan_umum','min, informasi apa saja yang tersedia','Saya dapat membantu lokasi bengkel, jadwal, servis motor, stok barang, dan rekomendasi produk.','');
INSERT INTO "chatbot_data" VALUES(189,'akhir_percakapan','terima kasih ya','Sama-sama, semoga membantu.','');
INSERT INTO "chatbot_data" VALUES(190,'akhir_percakapan','makasih ya','Sama-sama, hati-hati di jalan.','');
INSERT INTO "chatbot_data" VALUES(191,'akhir_percakapan','matur nuwun ya','Sama-sama, semoga membantu.','');
INSERT INTO "chatbot_data" VALUES(192,'akhir_percakapan','sudah cukup ya','Baik, terima kasih telah menggunakan layanan chatbot bengkel.','');
INSERT INTO "chatbot_data" VALUES(193,'akhir_percakapan','cukup ya','Baik, semoga informasi yang diberikan membantu.','');
INSERT INTO "chatbot_data" VALUES(194,'akhir_percakapan','itu saja ya','Baik, terima kasih sudah menghubungi bengkel kami.','');
INSERT INTO "chatbot_data" VALUES(195,'akhir_percakapan','tidak ada pertanyaan lagi ya','Baik, terima kasih sudah menghubungi bengkel kami.','');
INSERT INTO "chatbot_data" VALUES(196,'akhir_percakapan','sudah jelas ya','Baik, terima kasih telah menggunakan layanan chatbot bengkel.','');
INSERT INTO "chatbot_data" VALUES(197,'akhir_percakapan','oke makasih ya','Sama-sama, semoga harimu menyenangkan.','');
INSERT INTO "chatbot_data" VALUES(198,'akhir_percakapan','bye ya','Terima kasih telah menggunakan layanan chatbot bengkel.','');
INSERT INTO "chatbot_data" VALUES(199,'akhir_percakapan','sampai jumpa ya','Sampai jumpa kembali.','');
INSERT INTO "chatbot_data" VALUES(200,'akhir_percakapan','ok sip ya','Baik, semoga informasi yang diberikan membantu.','');
INSERT INTO "chatbot_data" VALUES(201,'jadwal_bengkel','min, bengkel buka jam berapa','Bengkel buka pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(202,'jadwal_bengkel','min, jam operasional bengkel','Bengkel buka Senin-Sabtu pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(203,'jadwal_bengkel','min, hari ini buka tidak','Bengkel buka Senin-Sabtu pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(204,'jadwal_bengkel','min, buka sampai jam berapa','Bengkel melayani sampai pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(205,'jadwal_bengkel','min, bengkel tutup jam berapa','Bengkel tutup pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(206,'jadwal_bengkel','min, hari minggu buka tidak','Bengkel libur pada hari Minggu.','');
INSERT INTO "chatbot_data" VALUES(207,'jadwal_bengkel','min, sabtu buka tidak','Bengkel buka hari Senin-Sabtu.','');
INSERT INTO "chatbot_data" VALUES(208,'jadwal_bengkel','min, bisa servis sore','Bengkel melayani servis sampai pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(209,'jadwal_bengkel','min, jadwal bengkel gimana','Bengkel buka Senin-Sabtu pukul 08.00-17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(210,'jadwal_bengkel','min, buka dari pagi jam berapa','Bengkel buka mulai pukul 08.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(211,'jadwal_bengkel','min, bengkel libur hari apa','Bengkel libur hari Minggu.','');
INSERT INTO "chatbot_data" VALUES(212,'jadwal_bengkel','min, masih buka sekarang','Bengkel buka sampai pukul 17.00 WIB.','');
INSERT INTO "chatbot_data" VALUES(213,'lokasi_bengkel','alamat bengkel dimana min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(214,'lokasi_bengkel','lokasi bengkel dimana min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(215,'lokasi_bengkel','bengkel ada dimana min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(216,'lokasi_bengkel','share lokasi bengkel min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(217,'lokasi_bengkel','ada maps bengkel min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(218,'lokasi_bengkel','kirim alamat bengkel min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(219,'lokasi_bengkel','bengkel dekat mana min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(220,'lokasi_bengkel','rute ke bengkel gimana min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(221,'lokasi_bengkel','posisi bengkel dimana min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(222,'lokasi_bengkel','lokasi lengkap bengkel min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(223,'lokasi_bengkel','maps kurnia motor min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(224,'lokasi_bengkel','saya mau ke bengkel min','Bengkel berada di depan Masjid Senduro.','open_maps');
INSERT INTO "chatbot_data" VALUES(225,'kontak_admin','min, nomor wa bengkel berapa','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(226,'kontak_admin','min, wa bengkel berapa','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(227,'kontak_admin','min, nomor whatsapp bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(228,'kontak_admin','min, bisa hubungi lewat whatsapp','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(229,'kontak_admin','min, kontak admin ada','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(230,'kontak_admin','min, nomor telepon bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(231,'kontak_admin','min, minta nomor admin','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(232,'kontak_admin','min, saya mau chat petugas','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(233,'kontak_admin','min, hubungi petugas bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(234,'kontak_admin','min, nomor bengkel berapa','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(235,'kontak_admin','min, kontak bengkel','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(236,'kontak_admin','min, admin bisa dihubungi','Nomor WhatsApp kami adalah 085606213825.','open_wa');
INSERT INTO "chatbot_data" VALUES(237,'harga_servis','ganti oli motor berapa ya','Biaya ganti oli mulai Rp50.000, belum termasuk harga oli tertentu.','');
INSERT INTO "chatbot_data" VALUES(238,'harga_servis','servis motor berapa ya','Biaya servis motor mulai dari Rp75.000.','');
INSERT INTO "chatbot_data" VALUES(239,'harga_servis','servis lengkap habis berapa ya','Biaya servis lengkap mulai dari Rp150.000.','');
INSERT INTO "chatbot_data" VALUES(240,'harga_servis','tune up motor berapa ya','Biaya tune up mulai dari Rp100.000.','');
INSERT INTO "chatbot_data" VALUES(241,'harga_servis','servis ringan berapa ya','Biaya servis ringan mulai dari Rp75.000.','');
INSERT INTO "chatbot_data" VALUES(242,'harga_servis','cek motor bayar tidak ya','Pengecekan motor gratis.','');
INSERT INTO "chatbot_data" VALUES(243,'harga_servis','biaya cek kerusakan motor ya','Pengecekan motor gratis.','');
INSERT INTO "chatbot_data" VALUES(244,'harga_servis','tarif servis matic ya','Biaya servis motor matic mulai dari Rp75.000.','');
INSERT INTO "chatbot_data" VALUES(245,'harga_servis','harga servis injeksi ya','Biaya servis injeksi menyesuaikan kondisi motor.','');
INSERT INTO "chatbot_data" VALUES(246,'harga_servis','berapa biaya perbaikan rem ya','Biaya perbaikan rem menyesuaikan kondisi dan sparepart.','');
INSERT INTO "chatbot_data" VALUES(247,'harga_servis','biaya ganti ban ya','Biaya penggantian ban menyesuaikan jenis ban.','');
INSERT INTO "chatbot_data" VALUES(248,'harga_servis','harga tune up bengkel ya','Biaya tune up mulai dari Rp100.000.','');
INSERT INTO "chatbot_data" VALUES(249,'layanan_servis','min, motor saya brebet','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(250,'layanan_servis','min, motor brebet saat digas','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(251,'layanan_servis','min, motor brebet di tanjakan','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(252,'layanan_servis','min, motor brebet saat dingin','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(253,'layanan_servis','min, motor susah hidup','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(254,'layanan_servis','min, rem motor keras','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(255,'layanan_servis','min, mesin motor cepat panas','Sedang menganalisis keluhan motor.','diagnosa');
INSERT INTO "chatbot_data" VALUES(256,'layanan_servis','min, bisa servis motor matic','Bengkel melayani servis motor matic.','');
INSERT INTO "chatbot_data" VALUES(257,'layanan_servis','min, bisa servis injeksi','Bengkel menerima servis injeksi.','');
INSERT INTO "chatbot_data" VALUES(258,'layanan_servis','min, bisa tune up motor','Bengkel melayani tune up motor.','');
INSERT INTO "chatbot_data" VALUES(259,'layanan_servis','min, bisa ganti ban','Bengkel melayani penggantian ban.','');
INSERT INTO "chatbot_data" VALUES(260,'layanan_servis','min, bisa ganti oli','Bengkel melayani penggantian oli.','');
INSERT INTO "chatbot_data" VALUES(261,'layanan_servis','min, bisa perbaiki rem motor','Bengkel melayani perbaikan rem motor.','');
INSERT INTO "chatbot_data" VALUES(262,'layanan_servis','min, servis motor karburator bisa','Bengkel melayani servis motor karburator.','');
INSERT INTO "chatbot_data" VALUES(263,'layanan_servis','min, servis motor beat bisa','Bengkel melayani servis motor Beat.','');
INSERT INTO "chatbot_data" VALUES(264,'layanan_servis','min, servis motor vario bisa','Bengkel melayani servis motor Vario.','');
INSERT INTO "chatbot_data" VALUES(265,'cek_stok','stok oli yamalube matic dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(266,'cek_stok','ada oli ahm mpx 2 dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(267,'cek_stok','oli enduro matic ready dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(268,'cek_stok','stok busi ngk cpr9ea dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(269,'cek_stok','ada busi denso u22epr9 dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(270,'cek_stok','stok aki gs astra dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(271,'cek_stok','aki yuasa masih ada dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(272,'cek_stok','ban fdr ready dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(273,'cek_stok','ban irc masih tersedia dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(274,'cek_stok','kampas rem federal ada dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(275,'cek_stok','kampas rem indoparts ready dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(276,'cek_stok','filter udara honda ada dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(277,'cek_stok','filter udara yamaha tersedia dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(278,'cek_stok','cvt belt bando ada dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(279,'cek_stok','rantai sss ready dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(280,'cek_stok','stok oli untuk beat dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(281,'cek_stok','stok busi untuk vario dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(282,'cek_stok','stok aki untuk scoopy dong','Sedang cek stok barang.','check_stock');
INSERT INTO "chatbot_data" VALUES(283,'info_barang','min, informasi oli yamalube matic','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(284,'info_barang','min, harga oli ahm mpx 2','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(285,'info_barang','min, detail oli enduro matic','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(286,'info_barang','min, info busi ngk cpr9ea','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(287,'info_barang','min, harga busi denso u22epr9','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(288,'info_barang','min, informasi aki gs astra','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(289,'info_barang','min, detail aki yuasa','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(290,'info_barang','min, harga ban fdr sport','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(291,'info_barang','min, info ban irc nr76','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(292,'info_barang','min, harga kampas rem federal','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(293,'info_barang','min, detail kampas rem indoparts','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(294,'info_barang','min, info filter udara honda','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(295,'info_barang','min, harga filter udara yamaha','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(296,'info_barang','min, detail cvt belt bando','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(297,'info_barang','min, harga rantai sss','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(298,'info_barang','min, harga oli untuk beat','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(299,'info_barang','min, info aki untuk vario','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(300,'info_barang','min, detail sparepart motor','Info barang.','info_barang');
INSERT INTO "chatbot_data" VALUES(301,'rekom_produk','oli yang cocok untuk beat dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(302,'rekom_produk','rekomendasi oli vario dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(303,'rekom_produk','oli bagus untuk scoopy dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(304,'rekom_produk','oli untuk motor matic dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(305,'rekom_produk','busi yang cocok untuk beat dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(306,'rekom_produk','busi untuk vario apa dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(307,'rekom_produk','aki terbaik untuk nmax dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(308,'rekom_produk','aki untuk pcx apa dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(309,'rekom_produk','ban yang cocok untuk beat dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(310,'rekom_produk','produk cocok untuk mio dong','Rekomendasi produk.','saran_produk');
INSERT INTO "chatbot_data" VALUES(311,'daftar_barang','oli yang tersedia ada apa saja dong','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(312,'daftar_barang','oli apa saja yang ada dong','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(313,'daftar_barang','daftar oli yang tersedia dong','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(314,'daftar_barang','pilihan oli di bengkel apa saja dong','Berikut daftar oli yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(315,'daftar_barang','busi yang tersedia ada apa saja dong','Berikut daftar busi yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(316,'daftar_barang','daftar aki yang ada dong','Berikut daftar aki yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(317,'daftar_barang','ban apa saja yang tersedia dong','Berikut daftar ban yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(318,'daftar_barang','sparepart yang tersedia apa saja dong','Berikut daftar sparepart yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(319,'daftar_barang','barang yang tersedia di bengkel apa saja dong','Berikut daftar barang yang tersedia.','list_barang');
INSERT INTO "chatbot_data" VALUES(320,'daftar_barang','ada pilihan filter udara apa saja dong','Berikut daftar filter udara yang tersedia.','list_barang');
CREATE TABLE "kategori_barang" (
	"id_kategori"	INTEGER,
	"nama_kategori"	TEXT NOT NULL,
	PRIMARY KEY("id_kategori" AUTOINCREMENT)
);
INSERT INTO "kategori_barang" VALUES(1,'oli');
INSERT INTO "kategori_barang" VALUES(2,'busi');
INSERT INTO "kategori_barang" VALUES(3,'aki');
INSERT INTO "kategori_barang" VALUES(4,'ban');
INSERT INTO "kategori_barang" VALUES(5,'kampas rem');
INSERT INTO "kategori_barang" VALUES(6,'sparepart');
INSERT INTO "kategori_barang" VALUES(7,'filter udara');
INSERT INTO "kategori_barang" VALUES(8,'lampu');
INSERT INTO "kategori_barang" VALUES(9,'filter oli');
INSERT INTO "kategori_barang" VALUES(10,'kampas kopling');
INSERT INTO "kategori_barang" VALUES(11,'knalpot');
INSERT INTO "kategori_barang" VALUES(12,'spion');
INSERT INTO "kategori_barang" VALUES(13,'roller');
INSERT INTO "kategori_barang" VALUES(14,'switch');
INSERT INTO "kategori_barang" VALUES(15,'starter motor');
INSERT INTO "kategori_barang" VALUES(16,'karburator');
INSERT INTO "kategori_barang" VALUES(17,'cdi');
INSERT INTO "kategori_barang" VALUES(18,'rem cakram');
INSERT INTO "kategori_barang" VALUES(19,'velg');
INSERT INTO "kategori_barang" VALUES(20,'rantai');
CREATE TABLE log_chat (

    id_chat INTEGER PRIMARY KEY AUTOINCREMENT,

    pertanyaan TEXT NOT NULL,

    intent TEXT,

    jawaban TEXT,

    waktu DATETIME DEFAULT CURRENT_TIMESTAMP
, klasifikasi TEXT, pertanyaan_normalisasi TEXT);
CREATE TABLE riwayat_stok (

    id_riwayat INTEGER PRIMARY KEY AUTOINCREMENT,

    id_admin INTEGER NOT NULL,

    id_barang INTEGER NOT NULL,

    aksi TEXT NOT NULL,

    stok_lama INTEGER,

    stok_baru INTEGER,

    tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_admin) REFERENCES users(id_admin),

    FOREIGN KEY (id_barang) REFERENCES barang(id_barang)
);
CREATE TABLE "users" (
	"id_admin"	INTEGER,
	"username"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id_admin" AUTOINCREMENT)
);
INSERT INTO "users" VALUES(1,'admin','pbkdf2:sha256:1000000$2aee272b1fdb1055$f31fe90dedaecade2ef964c87593d5641640c4c48ad23c3dd63a985d7fc2d223');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('barang',46);
INSERT INTO "sqlite_sequence" VALUES('users',1);
INSERT INTO "sqlite_sequence" VALUES('kategori_barang',20);
INSERT INTO "sqlite_sequence" VALUES('log_chat',82);
INSERT INTO "sqlite_sequence" VALUES('riwayat_stok',2);
INSERT INTO "sqlite_sequence" VALUES('chatbot_data',320);
COMMIT;
