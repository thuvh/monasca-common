/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package monasca.common.hibernate.db;

import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;

import org.hibernate.annotations.Type;

@Entity
@Table(name = "metric_definition")
public class MetricDefinitionDb {

  @Id
  @Column(name = "id", length = 20, updatable = false, nullable = false)
  @Lob
  @Type(type = "org.hibernate.type.UUIDBinaryType")
  private UUID id;

  @Column(name = "name", length = 255, nullable = false)
  private String name;

  @Column(name = "tenant_id", length = 36, nullable = false)
  private String tenant_id;

  @Column(name = "region", length = 255, nullable = false)
  private String region;

  public MetricDefinitionDb() {
    this(DbUtils.toUUID(DbUtils.DEFAULT_VALUE), "", "", "");
  }

  public MetricDefinitionDb(UUID id, String name, String tenant_id, String region) {
    super();
    this.id = id;
    this.name = name;
    this.tenant_id = tenant_id;
    this.region = region;
  }

  public MetricDefinitionDb(byte[] id, String name, String tenant_id, String region) {
    this(DbUtils.toUUID(id), name, tenant_id, region);
  }

  public byte[] getId() {
    return DbUtils.toByteArray(this.id);
  }

  public void setId(byte[] id) {
    this.id = DbUtils.toUUID(id);
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getTenant_id() {
    return tenant_id;
  }

  public void setTenant_id(String tenant_id) {
    this.tenant_id = tenant_id;
  }

  public String getRegion() {
    return region;
  }

  public void setRegion(String region) {
    this.region = region;
  }

  public UUID getPkey() {
    return this.id;
  }

}
