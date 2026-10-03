package com.example.modelsguns;

import net.fabricmc.api.ModInitializer;
import net.minecraft.item.Item;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

public class ModelsGuns implements ModInitializer {
    public static final String MOD_ID = "modelsguns";

    public static final String[] GUNS = {"mk18", "glock17", "ak47", "deagle", "mp5a5", "m870", "awm"};

    @Override
    public void onInitialize() {
        for (String id : GUNS) {
            Registry.register(Registries.ITEM, new Identifier(MOD_ID, id),
                    new GunItem(id, new Item.Settings().maxCount(1)));
        }
    }
}
