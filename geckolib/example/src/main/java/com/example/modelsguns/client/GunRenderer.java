package com.example.modelsguns.client;

import com.example.modelsguns.GunItem;
import com.example.modelsguns.ModelsGuns;
import com.geckolib.constant.DataTickets;
import com.geckolib.model.DefaultedItemGeoModel;
import com.geckolib.renderer.GeoItemRenderer;
import com.geckolib.renderer.base.BoneSnapshots;
import com.geckolib.renderer.base.GeoRenderState;
import com.geckolib.renderer.base.RenderPassInfo;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemDisplayContext;

/**
 * Gun renderer: the model carries first-person arms in the bones
 * "right_arm" and "left_arm"; they are only drawn in first person
 * (in the inventory, on the ground or in third person only the gun is drawn).
 */
public class GunRenderer extends GeoItemRenderer<GunItem> {
    public GunRenderer(String gunId) {
        super(new DefaultedItemGeoModel<>(Identifier.fromNamespaceAndPath(ModelsGuns.MOD_ID, gunId)));
    }

    @Override
    public void adjustModelBonesForRender(RenderPassInfo<GeoRenderState> renderPassInfo, BoneSnapshots snapshots) {
        ItemDisplayContext context = renderPassInfo.getGeckolibData(DataTickets.ITEM_RENDER_PERSPECTIVE);
        boolean firstPerson = context == ItemDisplayContext.FIRST_PERSON_RIGHT_HAND
                || context == ItemDisplayContext.FIRST_PERSON_LEFT_HAND;
        if (!firstPerson) {
            snapshots.ifPresent("right_arm", bone -> bone.skipRender(true));
            snapshots.ifPresent("left_arm", bone -> bone.skipRender(true));
        }
    }
}
