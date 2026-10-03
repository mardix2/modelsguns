package com.example.modelsguns;

import java.util.function.Consumer;

import com.geckolib.animatable.GeoItem;
import com.geckolib.animatable.client.GeoRenderProvider;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.animation.AnimationController;
import com.geckolib.animation.RawAnimation;
import com.geckolib.animation.object.PlayState;
import com.geckolib.model.DefaultedItemGeoModel;
import com.geckolib.renderer.GeoItemRenderer;
import com.geckolib.util.GeckoLibUtil;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import org.jspecify.annotations.Nullable;

/**
 * Gun item for Minecraft 26.2 + Fabric + GeckoLib 5 (Mojang names).
 *
 * GeckoLib loads:
 *   assets/<modid>/geckolib/models/item/<id>.geo.json
 *   assets/<modid>/geckolib/animations/item/<id>.animation.json
 *   assets/<modid>/textures/item/<id>.png
 * and the item is drawn through assets/<modid>/items/<id>.json
 * ("minecraft:special" -> "geckolib:geckolib"), whose base model
 * models/item/<id>.json holds the hand/GUI transforms.
 *
 * Right click plays the "shoot" animation.
 */
public class GunItem extends Item implements GeoItem {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private final String gunId;

    public GunItem(String gunId, Properties properties) {
        super(properties);
        this.gunId = gunId;
        GeoItem.registerSyncedAnimatable(this);
    }

    @Override
    public void createGeoRenderer(Consumer<GeoRenderProvider> consumer) {
        consumer.accept(new GeoRenderProvider() {
            private @Nullable GeoItemRenderer<GunItem> renderer;

            @Override
            public GeoItemRenderer<?> getGeoItemRenderer() {
                if (this.renderer == null) {
                    this.renderer = new GeoItemRenderer<>(new DefaultedItemGeoModel<>(
                            Identifier.fromNamespaceAndPath(ModelsGuns.MOD_ID, gunId)));
                }
                return this.renderer;
            }
        });
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<GunItem>("main", 0, test -> PlayState.STOP)
                .triggerableAnim("shoot", RawAnimation.begin().thenPlay("animation." + gunId + ".shoot"))
                .triggerableAnim("reload", RawAnimation.begin().thenPlay("animation." + gunId + ".reload")));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel serverLevel) {
            triggerAnim(player, GeoItem.getOrAssignId(stack, serverLevel), "main", "shoot");
        }
        return InteractionResult.SUCCESS;
    }
}
