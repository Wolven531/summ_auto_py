@echo off
title MonsterDownloader - SummAutoPy

echo %Time% Initiating download process for dark mons...
start "Dark Mon Downloader (Startup=%Time%)" python MonsterDownloader.py dark

echo %Time% Initiating download process for fire mons...
start "Fire Mon Downloader (Startup=%Time%)" python MonsterDownloader.py fire

echo %Time% Initiating download process for light mons...
start "Light Mon Downloader (Startup=%Time%)" python MonsterDownloader.py light

echo %Time% Initiating download process for water mons...
start "Water Mon Downloader (Startup=%Time%)" python MonsterDownloader.py water

echo %Time% Initiating download process for wind mons...
start "Wind Mon Downloader (Startup=%Time%)" python MonsterDownloader.py wind
