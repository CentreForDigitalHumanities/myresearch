<template>
    <footer class="uu-footer">
        <div class="col-12 col-md-4">
            <img
                :alt="$t('Utrecht University')"
                :src="
                    useStaticFile(
                        '/images/logo-footer-nl.svg'
                    )
                "
            />
        </div>
        <div class="col-12 col-md-8 text-md-end">
            <p>
                MyResearch
                <br />
                {{ $t("Faculty of Humanities") }}
            </p>
        </div>
    </footer>
</template>
