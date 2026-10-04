package com.example.modelsguns.client;

import com.example.modelsguns.GunItem;
import com.example.modelsguns.ModelsGuns;
import com.geckolib.constant.DataTickets;
import com.geckolib.model.DefaultedItemGeoModel;
import com.geckolib.renderer.GeoItemRenderer;
import com.geckolib.renderer.base.BoneSnapshots;
import com.geckolib.renderer.base.GeoRenderState;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.builtin.CustomBoneTextureGeoLayer;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemDisplayContext;

/**
 * Gun renderer.
 *
 * The model carries Minecraft arms in the bones "right_arm" and "left_arm".
 * Their UVs follow the 64x64 player skin layout, so they are drawn with the
 * local player's own skin by two CustomBoneTextureGeoLayer layers (the gun
 * texture also has Steve-like arms in that layout as a fallback).  The arms
 * are only drawn in first person.
 */
public class GunRenderer extends GeoItemRenderer<GunItem> {
    private static final Identifier STEVE = Identifier.withDefaultNamespace("textures/entity/player/wide/steve.png");

    public GunRenderer(String gunId) {
        super(new DefaultedItemGeoModel<>(Identifier.fromNamespaceAndPath(ModelsGuns.MOD_ID, gunId)));
        withRenderLayer(new SkinArmLayer(this, "right_arm"));
        withRenderLayer(new SkinArmLayer(this, "left_arm"));
    }

    static boolean isFirstPerson(GeoRenderState renderState) {
        ItemDisplayContext context = renderState.getGeckolibData(DataTickets.ITEM_RENDER_PERSPECTIVE);
        return context == ItemDisplayContext.FIRST_PERSON_RIGHT_HAND
                || context == ItemDisplayContext.FIRST_PERSON_LEFT_HAND;
    }

    @Override
    public void adjustModelBonesForRender(RenderPassInfo<GeoRenderState> renderPassInfo, BoneSnapshots snapshots) {
        if (!isFirstPerson(renderPassInfo.renderState())) {
            snapshots.ifPresent("right_arm", bone -> bone.skipRender(true));
            snapshots.ifPresent("left_arm", bone -> bone.skipRender(true));
        }
    }

    /** Draws one arm bone with the local player's skin, in first person only. */
    static class SkinArmLayer extends CustomBoneTextureGeoLayer<GunItem, GeoItemRenderer.RenderData, GeoRenderState> {
        SkinArmLayer(GunRenderer renderer, String bone) {
            super(renderer, bone, STEVE);
        }

        @Override
        public boolean shouldRenderBone(GeoRenderState renderState) {
            return isFirstPerson(renderState);
        }

        @Override
        protected Identifier getTextureResource(GeoRenderState renderState) {
            LocalPlayer player = Minecraft.getInstance().player;
            // 26.x: PlayerSkin.body() is the skin texture asset
            return player != null ? player.getSkin().body().texturePath() : STEVE;
        }
    }
}
