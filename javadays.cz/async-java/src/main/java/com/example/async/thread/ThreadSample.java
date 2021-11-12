package com.example.async.thread;

import java.util.UUID;

public class ThreadSample {

    public static void main(String[] args) {
        final String uuid = UUID.randomUUID().toString();
        System.out.println("generating UUID:" + uuid);
        saveFile(uuid);
        System.out.println("file stored with id:" + uuid);
    }

    private static void saveFile(String uuid) {

        new Thread( () -> {
            try {
                Thread.sleep(1000L);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("file saved");
        }).start();
    }
}
